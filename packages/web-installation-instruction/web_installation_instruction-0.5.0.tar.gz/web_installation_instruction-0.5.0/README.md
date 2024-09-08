<div align="center">

# `web-installation-instruction`

**Tool rendering html page from install.cfg file.**

[![PyPI - Version](https://img.shields.io/pypi/v/web-installation-instruction)](https://pypi.org/project/web-installation-instruction/)
[![PyPI - License](https://img.shields.io/pypi/l/web-installation-instruction)](https://github.com/instructions-d-installation/web-installation-instruction/blob/main/LICENSE)

</div>

## Usage

1. Create an `install.cfg` which adheres to [`installation-instruction`](https://github.com/instructions-d-installation/installation-instruction).
    * Be sure to stay in the confinements of [`nunjucks`](https://mozilla.github.io/nunjucks/templating.html) and [`jinja2`](https://jinja.palletsprojects.com/en/3.1.x/templates/).
2. Compile the `install.cfg` to an html file with `ibi-build-html`.

```
 Usage: ibi-build-html [OPTIONS]

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --input   -i      TEXT  Path to config file. [default: ./install.cfg]                                                                                                                                                        │
│ --output  -o      TEXT  Path to output directory. [default: ./public]                                                                                                                                                        │
│ --help                  Show this message and exit.                                                                                                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Github Action

Take a look at [web-installation-instruction-action](https://github.com/instructions-d-installation/web-installation-instruction-action).

## Automatic Defaults

You must have such property in your schema and have some of the options below (take those that you actually support):

```yaml
__os__:
  - android
  - ios
  - windows
  - linux
  - macos
  - openbsd
  - freebsd
```


## Example

[![example](./pictures/example.png)](https://instructions-d-installation.github.io/web-installation-instruction)