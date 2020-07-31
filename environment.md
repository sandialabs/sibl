# Environment

## Server

### Create the environment

```bash
(base) $ conda create --name sibltest python=3.7 scipy matplotlib pandas pillow
(base) $ conda env remove --name sibltest
(base) $ conda env list
(base) $ conda create --name siblenv python=3.8 scipy matplotlib pandas pillow dash xlrd pylint pytest flake8
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
  - pylint
  - dash
  - pillow
  - xlrd
  - pytest
  - pandas
  - scipy
  - matplotlib
prefix: /Users/Apollo/opt/anaconda3/envs/siblenv
```


## Client setup

### 

Clients should create their conda virtual environment from the above server-generated [environment.yml](environment.yml) file using the following commands

```bash
(base) $ conda env create -f environment.yml
(base) $ conda env list  # verify the environment was installed
(base) $ conda activate siblenv
(siblenv) $
```



## References

* Conda [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
* Conda [cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)
* [Docker Hub](https://hub.docker.com/)
