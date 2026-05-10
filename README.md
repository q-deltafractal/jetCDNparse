# jetCDNparse

<div>
  <a href="https://www.python.org/">
    <img src="docs/badges/python.svg" height="28" alt="python3.11">
  </a>
  <a href="https://github.com">
    <img src="docs/badges/github.svg" height="28" alt="available on github">
  </a>
</div>

## compilation process

_Linux-based systems_

### requirements

- [ ] [uv](https://docs.astral.sh/uv/) python package manager
- [ ] [git](https://git-scm.com/install/) version control

_latest versions_

### preparation

```bash
# setup virtual env
uv sync
```

```bash
# setup configuration project
cp template.env .env
```

### compilation

```console
$ cd jetCDNparse
$ uv run main.py
INFO:jetCDNparse:booted
...
INFO:jetCDNparse:compilation success on ~/.../jetCDNparse/dist
```

<br>

## license

project is licensed under:

<table>
  <tr>
    <td>
      WTFPL
    </td>
    <td>
      <a href="LICENSE">LICENSE</a>
    </td>
    <td>
      https://www.wtfpl.net/about/
    </td>
  </tr>
</table>
