#!/bin/bash

# reference: ruxi/make_conda_env.sh
# https://gist.github.com/ruxi/949e3d326c5a8a24ecffa8a225b2be2a 
echo This shell script recreates the conda environment 
echo for use with the xyfigure and zplot modules.

# echo "Select an environment name (e.g., siblenv):"
# read y
y='siblenv' # the conda environment of interest
echo Creating conda environment $y

echo Verifying that conda is up-to-date:
conda activate base
conda update -n base -c defaults conda

echo Current conda environments:
conda env list

# remove existing environment, if it exists
echo Removing existing $y environment, should it exist...
conda env remove --name $y
echo Conda environments after attempt at removal of old environment:
conda env list

echo Recreating a new $y environment...
conda create --name $y python=3.8 black dash flake8 ipykernel matplotlib pandas pillow pytest pytest-cov scipy seaborn xlrd

# echo Activating the new $y environment...
# conda init bash
# conda activate $y
# 
# echo Finally, some pip items...
# echo The pip listing prior to install...
# pip list
# 
# echo Installing the zmath module in developer mode...
# pip install -e .
# 
# echo The pip listing after install...
# pip list

echo -----------------------------------------------
echo The shell script setup.sh and is now completed.
echo -----------------------------------------------
