#!/usr/bin/env python

import argparse
from datetime import datetime, timedelta, UTC
import json
import shutil
import logging
from pathlib import Path

import httpx
from environs import Env
from jinja2 import Environment, FileSystemLoader, select_autoescape

PROJECT_NAME = 'jetCDNparse'

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

# files dirs
GLOBAL_DIR = Path(__file__).parent
CONFIG_DIR = GLOBAL_DIR.parent
STATIC_DIR = GLOBAL_DIR / 'static'

# dist dirs/names
LINKS_NAME = 'links'
RES_NAME = 'static'
DIST_DIR = CONFIG_DIR / 'dist'
DIST_LINKS_DIR = DIST_DIR / LINKS_NAME

# other
LAST_SYNC_FILE = CONFIG_DIR / 'last-sync.json'

# logging
logger = logging.getLogger(PROJECT_NAME)

# jinja
jinja_env = Environment(
    loader=FileSystemLoader(STATIC_DIR),
    autoescape=select_autoescape(['html', 'xml']),
)


def main(args: list[str] | None = None) -> None:
    """main logic"""

    # parser
    parser = argparse.ArgumentParser(prog=PROJECT_NAME)

    parser.add_argument('-f', '--force', action='store_true', help='force API sync')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose logging')

    options = parser.parse_args(args)

    # env
    env = Env(expand_vars=True)
    env.read_env()

    min_sync_delay: timedelta = env.timedelta(
        'MIN_UPDATE_INTERVAL',
        default=timedelta(hours=12),
    )
    user_agent: str = env(
        'USER_AGENT',
        default=(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/147.0.0.0 Safari/537.36'
        ),
    )

    # logging
    logging.basicConfig(level=logging.DEBUG if options.verbose else logging.INFO)

    logger.info('booted')

    # request
    json_data = dict()

    last_sync: datetime | None = None
    if Path.is_file(LAST_SYNC_FILE):
        with open(LAST_SYNC_FILE, 'r', encoding='UTF-8') as f:
            dump = json.loads(f.read())
            last_sync = datetime.strptime(dump.get('last_sync'), TIME_FORMAT)
            json_data = dump.get('data', dict())

    if (
        options.force
        or not last_sync
        or (last_sync + min_sync_delay - timedelta(minutes=1) < datetime.now(tz=UTC))
    ):
        logger.info('making request')

        r = httpx.get(
            url='https://data.services.jetbrains.com/products',
            params={'fields': ['name', 'releases']},
            headers={'User-Agent': user_agent},
        )

        if not r.is_success:
            parser.exit(1, 'request failed')

        json_data = r.json()

        with open(LAST_SYNC_FILE, 'w', encoding='UTF-8') as f:
            f.write(
                json.dumps(
                    {
                        'last_sync': (datetime.now(tz=UTC).strftime(TIME_FORMAT)),
                        'data': json_data,
                    }
                )
            )
    else:
        logger.info('used backup file, since the minimum delay time has not passed')

    global_context = {
        'links_start': LINKS_NAME,
        'timestamp': last_sync or datetime.now(tz=UTC).strftime(TIME_FORMAT),
        'res_dir_name': RES_NAME,
    }

    # pre-compile
    logger.info('(re)creating dist')
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    for new_dir in filter(
        lambda a: a[0].startswith('DIST_'),
        dict(globals()).items(),
    ):
        logger.debug('new: %s', new_dir)
        Path.mkdir(new_dir[1])
    logger.debug('copying static files')
    shutil.copytree(STATIC_DIR / 'resources', DIST_DIR / RES_NAME)

    # compile
    logger.info('compiling html files')

    names: list[str] = list()

    item: dict
    for item in sorted(json_data, key=lambda a: a.get('name')):
        name = item.get('name').replace(' ', '_')
        releases = item.get('releases', tuple())

        if releases:
            names.append(name)
            (
                jinja_env.get_template('gen/product_links.html')
                .stream(releases=releases, name=name, **global_context)
                .dump(str(DIST_LINKS_DIR / f'{name}.html'))
            )
            logger.debug('product %s - done', name)
        else:
            logger.debug('product %s - skipped (no releases)', name)

    (
        jinja_env.get_template('gen/products.html')
        .stream(names=names, **global_context)
        .dump(str(DIST_DIR / 'index.html'))
    )
    logger.debug('index - done')

    logger.info('compilation success on %s', DIST_DIR)


if __name__ == '__main__':
    main()

