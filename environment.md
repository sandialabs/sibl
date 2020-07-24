# Environment

## Server

### Create the environment

```bash
(base) $ conda create --name sibltest python=3.7 scipy matplotlib pandas pillow
(base) $ conda env remove --name sibltest
(base) $ conda env list
(base) $ conda create --name siblenv python=3.8 scipy matplotlib pandas pillow dash xlrd pylint pytest
(base) $ conda activate siblenv
(siblenv) $ pip install xyfigure
```

### Create the environment configuration file

```bash
(siblenv) $ conda env export > environment.yml
```

The `environment.yml` file will contain the following

```yml
name: siblenv
channels:
  - defaults
dependencies:
  - astroid=2.4.2=py38_0
  - attrs=19.3.0=py_0
  - blas=1.0=mkl
  - brotlipy=0.7.0=py38haf1e3a3_1000
  - ca-certificates=2020.6.24=0
  - certifi=2020.6.20=py38_0
  - cffi=1.14.0=py38hc512035_1
  - click=7.1.2=py_0
  - cycler=0.10.0=py38_0
  - dash=1.4.1=py_0
  - dash-core-components=1.3.1=py_0
  - dash-html-components=1.0.1=py_0
  - dash-renderer=1.1.2=py_0
  - dash-table=4.4.1=py_0
  - flask=1.1.2=py_0
  - flask-compress=1.5.0=py_0
  - freetype=2.10.2=ha233b18_0
  - future=0.18.2=py38_1
  - intel-openmp=2019.4=233
  - isort=4.3.21=py38_0
  - itsdangerous=1.1.0=py_0
  - jinja2=2.11.2=py_0
  - jpeg=9b=he5867d9_2
  - kiwisolver=1.2.0=py38h04f5b5a_0
  - lazy-object-proxy=1.4.3=py38h1de35cc_0
  - lcms2=2.11=h92f6f08_0
  - libcxx=10.0.0=1
  - libedit=3.1.20191231=h1de35cc_1
  - libffi=3.3=hb1e8313_2
  - libgfortran=3.0.1=h93005f0_2
  - libpng=1.6.37=ha441bb4_0
  - libtiff=4.1.0=hcb84e12_1
  - lz4-c=1.9.2=h0a44026_0
  - markupsafe=1.1.1=py38h1de35cc_1
  - matplotlib=3.2.2=0
  - matplotlib-base=3.2.2=py38h5670ca0_0
  - mccabe=0.6.1=py38_1
  - mkl=2019.4=233
  - mkl-service=2.3.0=py38hfbe908c_0
  - mkl_fft=1.1.0=py38hc64f4ea_0
  - mkl_random=1.1.1=py38h959d312_0
  - more-itertools=8.4.0=py_0
  - ncurses=6.2=h0a44026_1
  - numpy=1.18.5=py38h1da2735_0
  - numpy-base=1.18.5=py38h3304bdc_0
  - olefile=0.46=py_0
  - openssl=1.1.1g=h1de35cc_0
  - packaging=20.4=py_0
  - pandas=1.0.5=py38h959d312_0
  - pillow=7.2.0=py38ha54b6ba_0
  - pip=20.1.1=py38_1
  - plotly=4.8.2=py_0
  - pluggy=0.13.1=py38_0
  - py=1.9.0=py_0
  - pycparser=2.20=py_2
  - pylint=2.5.3=py38_0
  - pyparsing=2.4.7=py_0
  - pytest=5.4.3=py38_0
  - python=3.8.3=h26836e1_2
  - python-dateutil=2.8.1=py_0
  - pytz=2020.1=py_0
  - pyyaml=5.3.1=py38haf1e3a3_1
  - readline=8.0=h1de35cc_0
  - retrying=1.3.3=py_2
  - scipy=1.5.0=py38hbab996c_0
  - setuptools=49.2.0=py38_0
  - six=1.15.0=py_0
  - sqlite=3.32.3=hffcf06c_0
  - tk=8.6.10=hb0a8c7a_0
  - toml=0.10.1=py_0
  - tornado=6.0.4=py38h1de35cc_1
  - wcwidth=0.2.5=py_0
  - werkzeug=1.0.1=py_0
  - wheel=0.34.2=py38_0
  - wrapt=1.11.2=py38h1de35cc_0
  - xlrd=1.2.0=py_0
  - xz=5.2.5=h1de35cc_0
  - yaml=0.2.5=haf1e3a3_0
  - zlib=1.2.11=h1de35cc_3
  - zstd=1.4.5=h41d2c2f_0
  - pip:
    - xyfigure==0.0.5
prefix: /Users/Apollo/opt/anaconda3/envs/siblenv
```


## Client setup

Clients should create their conda virtual environment from the above server-generated [environment.yml](environment.yml) file using the following commands

```bash
$ conda env create -f environment.yml
$ conda env list  # verify the environment was installed
```



## References

* Conda [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
* Conda [cheat sheet](https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf)
* [Docker Hub](https://hub.docker.com/)
