# Configuration

Following is the recommended configuration for a development environment.

## Virtual Environment

```bash
cd ~/sibl

/usr/local/bin/python3.9 -m pip install --upgrade pip setuptools wheel

# create a virtual environment
# VS Code docs reference:
# https://code.visualstudio.com/docs/python/environments#_create-a-virtual-environment
/usr/local/bin/python3.9 -m venv .venv  # create a virtual environment

# activate the venv with one of the following:
source .venv/bin/activate # for bash shell
source .venv/bin/activate.csh # for c shell
source .venv/bin/activate.fish # for fish shell
source .venv/bin/Activate.fish # for powershell

python --version  # e.g., Python 3.9.7

pip list

Package    Version
---------- -------
pip        21.2.1
setuptools 57.4.0
WARNING: You are using pip version 21.2.3; however, version 22.3.1 is available.
You should consider upgrading via the '~/sibl/.venv/bin/python3.9 -m pip install --upgrade pip' command.
(.venv) ~/copyright>

python -m pip install --upgrade pip
```

## Install modules as a developer

Reference: https://packaging.python.org/en/latest/tutorials/packaging-projects/

```bash
packaging_tutorial/
├── LICENSE
├── pyproject.toml
├── README.md
├── src/
│   └── your_package_name_here/
│       ├── __init__.py
│       └── example.py
└── tests/
```

Create a `pyproject.toml`, e.g., example `.toml` reference: https://peps.python.org/pep-0621/#example and general setuptools documentation: https://setuptools.pypa.io/en/latest/index.html

Installing from a local source tree, reference:

* https://packaging.python.org/en/latest/tutorials/installing-packages/#installing-from-a-local-src-tree, and
* development mode: https://setuptools.pypa.io/en/latest/userguide/development_mode.html

```bash
# create an editable install (aka development mode)
(.venv) ~/sibl>
python -m pip install -e geo/.[dev]  # developer
python -m pip install geo/.  # client
# note: `-e .` = `--editable .`
python -m pip install -e geo/src/bind/
python -m pip install -e cli/
```

Post-install package status:

```bash
(.venv) ~/sibl>
pip list
Package            Version Editable project location
------------------ ------- -------------------------
anyio                    3.6.2
appnope                  0.1.3
argon2-cffi              21.3.0
argon2-cffi-bindings     21.2.0
arrow                    1.2.3
asttokens                2.2.1
attrs                    22.2.0
backcall                 0.2.0
beautifulsoup4           4.11.1
black                    22.3.0
bleach                   6.0.0
cffi                     1.15.1
click                    8.1.3
comm                     0.1.2
contourpy                1.0.7
copyright                0.0.1
coverage                 7.0.5
cycler                   0.11.0
debugpy                  1.6.6
decorator                5.1.1
defusedxml               0.7.1
entrypoints              0.4
exceptiongroup           1.1.0
executing                1.2.0
fastjsonschema           2.16.2
flake8                   6.0.0
fonttools                4.38.0
fqdn                     1.5.1
idna                     3.4
imageio                  2.25.0
importlib-metadata       6.0.0
iniconfig                2.0.0
ipykernel                6.20.2
ipython                  8.8.0
ipython-genutils         0.2.0
isoduration              20.11.0
jedi                     0.18.2
Jinja2                   3.1.2
jsonpointer              2.3
jsonschema               4.17.3
jupyter_client           7.4.9
jupyter_core             5.1.5
jupyter-events           0.6.3
jupyter_server           2.1.0
jupyter_server_terminals 0.4.4
jupyterlab-pygments      0.2.2
kiwisolver               1.4.4
MarkupSafe               2.1.2
matplotlib               3.6.3
matplotlib-inline        0.1.6
mccabe                   0.7.0
mistune                  2.0.4
mypy                     0.991
mypy-extensions          0.4.3
nbclassic                0.5.0
nbclient                 0.7.2
nbconvert                7.2.9
nbformat                 5.7.3
nest-asyncio             1.5.6
networkx                 3.0
notebook                 6.5.2
notebook_shim            0.2.2
numpy                    1.24.1
packaging                23.0
pandas                   1.5.3
pandocfilters            1.5.0
parso                    0.8.3
pathspec                 0.11.0
pexpect                  4.8.0
pickleshare              0.7.5
Pillow                   9.4.0
pip                      22.3.1
platformdirs             2.6.2
pluggy                   1.0.0
prometheus-client        0.16.0
prompt-toolkit           3.0.36
psutil                   5.9.4
ptg                      0.0.4       /Users/chovey/sibl/geo/src
ptyprocess               0.7.0
pure-eval                0.2.2
pybind11                 2.10.3
pycodestyle              2.10.0
pycparser                2.21
pyflakes                 3.0.1
Pygments                 2.14.0
pyparsing                3.0.9
pyrsistent               0.19.3
pytest                   7.2.1
pytest-cov               4.0.0
python-dateutil          2.8.2
python-json-logger       2.0.4
pytz                     2022.7.1
PyWavelets               1.4.1
PyYAML                   6.0
pyzmq                    25.0.0
rfc3339-validator        0.1.4
rfc3986-validator        0.1.1
scikit-image             0.19.3
scipy                    1.10.0
seaborn                  0.12.2
Send2Trash               1.8.0
setuptools               57.4.0
sibl                     0.0.10
six                      1.16.0
sniffio                  1.3.0
soupsieve                2.3.2.post1
stack-data               0.6.2
terminado                0.17.1
tifffile                 2023.1.23.1
tinycss2                 1.2.1
tomli                    2.0.1
tornado                  6.2
traitlets                5.8.1
typing_extensions        4.4.0
uri-template             1.2.0
wcwidth                  0.2.6
webcolors                1.12
webencodings             0.5.1
websocket-client         1.4.2
xybind                   0.0.8       /Users/chovey/sibl/geo/src/bind
xyfigure                 0.0.9       /Users/chovey/sibl/cli/src
zipp                     3.11.0
```

Deactivate/Reactivate method:  To deactivate any current `venv`:

```bash
deactivate
```

Deactivate/Reactivate method:  To activate the `.venv` virtual environment:

```bash
# activate the venv with one of the following:
source .venv/bin/activate # for bash shell
source .venv/bin/activate.csh # for c shell
source .venv/bin/activate.fish # for fish shell
source .venv/bin/Activate.fish # for powershell
```

Run from the REPL:

```bash
(.venv) python
Python 3.9.7 (v3.9.7:1016ef3790, Aug 30 2021, 16:39:15)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from copyright import command_line as cl
>>> cl.version()
copyright version:
'0.0.1'
>>> quit()
```

Run from the command line:

```bash
(.venv) commands
---------
copyright
---------
This is the command line interface help for Sandia National Laboratories copyright Python module.
Available commands:
commands   (this command)
scinfo     Describes the installation details.
version    Prints the semantic verison of the current installation.
```

Run the tests with `pytest`:

```bash
(.venv) ~/sibl> cd geo
(.venv) ~/sibl/geo> pytest -v
```

And `pytest-cov` (coverage) with line numbers missing coverage:

```bash
(.venv) ~/sibl/geo> pytest --cov=copyright --cov-report term-missing
```

Success!  The `venv` virtual environment `.venv` has been created, 
and the `atmesh` module is now installed and tested.

## Typical Development Cycle

```bash
# develop code
# uninstall the now-outdated developer installation
pip uninstall copyright
# reinstall the module with the newly developed code
pip install -e .[dev]
```

## Modify VS Code if desired

In the user `settings.json`, add a reference to the Cubit install location.  

Reference: Enable IntelliSense for custom package locations, https://code.visualstudio.com/docs/python/editing#_enable-intellisense-for-custom-package-locations

Before:

```bash
    "python.autoComplete.extraPaths": [
        "~/python_modules"
    ],
```

After:

```bash
    "python.autoComplete.extraPaths": [
        "~/python_modules",
        "/Applications/Cubit-16.08/Cubit.app/Contents/MacOS"
    ],
    "python.envFile": "${workspaceFolder}/.venv",
```

## Continuous Integration (CI)

Any push to the `main` branch that contains at least one file with a `.py` extension will trigger CI.  The CI tests against the Black code formatter, against `flake8`, and assesses code coverage. 

## Continuous Deployment (CD)

The `.github/workflows/release.yml` automates the build of a release when a `git push` is specified with a version flag, such as `v1.0`, `v20.15.10`, etc.

### Git Tag

* Git Tag [reference](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
* View the existing tag (if any):

```bash
$ git tag
v1.0
v2.0

# Create a git tag with the `-a` flag:
$ git tag -a v1.4 -m "my version 1.4"

# Read the tag
$ git show v1.4
```

## References

* https://github.com/cycjimmy/semantic-release-action
* https://github.com/anirudh2/setup-jl
* https://github.com/marketplace/actions/action-for-semantic-release
* https://github.com/semantic-release/semantic-release
* https://github.com/python-semantic-release/python-semantic-release
* https://python-semantic-release.readthedocs.io/en/latest/automatic-releases/github-actions.html
