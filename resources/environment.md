# Environment

## Server

* IDE: [VS Code](https://code.visualstudio.com/)
* Linting: [flake8](https://pypi.org/project/flake8/)
* Auto-formatter: [Black](https://pypi.org/project/black/)
  * [Settings](https://dev.to/adamlombard/how-to-use-the-black-python-code-formatter-in-vscode-3lo0) for VS Code
* Testing: 
  * CI: GitHub [Actions](https://docs.github.com/en/actions)
  * [unittest](https://docs.python.org/3/library/unittest.html)

### Create the environment

```bash
(base) $ conda create --name sibltest python=3.7 scipy matplotlib pandas pillow
(base) $ conda env remove --name sibltest
(base) $ conda env list
(base) $ conda update -n base -c defaults conda
(base) $ conda create --name siblenv python=3.8 scipy matplotlib pandas pillow dash xlrd pytest pylint flake8 seaborn black ipykernel
(base) $ conda activate siblenv
(siblenv) $ pip install xyfigure
```

### Create the environment configuration file

Based on [sharing an environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#sharing-an-environment) documentation, to make a configuration file that is *cross-platorm*, use

```bash
(siblenv) $ conda env export --from-history > environment.yml
```

The `environment.yml` file will contain the following

```yml
name: siblenv
channels:
  - defaults
dependencies:
  - python=3.8
  - dash
  - flake8
  - matplotlib
  - black
  - scipy
  - xlrd
  - pillow
  - pytest
  - pylint
  - seaborn
  - pandas
prefix: /Users/Apollo/opt/anaconda3/envs/siblenv
```

## Client setup

### First Install

Clients should create their conda virtual environment from the above server-generated [environment.yml](environment.yml) file using the following commands

```bash
(base) $ conda env create -f environment.yml
(base) $ conda env list  # verify the environment was installed
(base) $ conda activate siblenv
(siblenv) $
```

## Subsequent Installs (Updates)

Update current install to the latest version:

```bash
(siblenv) $ pip install xyfigure --upgrade
```

To install a specific version, e.g., version `0.0.5`:

```bash
(siblenv) $ pip install --user xyfigure==0.0.5
```

## Optional Installs (In Development)

Optional installs required for Qt application development:

```bash
(siblenv) $ pip install pyside2 # installed version 5.15.1 on 2020-04-14
(siblenv) $ pip install toyplot # installed version 0.019.0 on 2020-04-14
```

## References

* Conda [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
* Conda [cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)
* [Docker Hub](https://hub.docker.com/)
