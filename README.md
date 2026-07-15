# jetCDNparse

a small JetBrains API parser

<br>

## compilation process

### requirements

- [ ] [uv](https://docs.astral.sh/uv/) python package manager
- [ ] [git](https://git-scm.com/install/) version control

### preparation

```bash
# clone repo
git clone https://github.com/q-deltafractal/jetCDNparse.git
cd jetCDNparse
```

```bash
# setup virtual env
uv sync
```

_now change the parser configuration in the [`config.toml`](config.toml) file to suit your needs_

### compilation

```console
$ cd jetCDNparse
$ uv run main.py
INFO:jetCDNparse:booted
...
INFO:jetCDNparse:compilation success on /home/.../jetCDNparse/dist
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
