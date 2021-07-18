#!/bin/bash

# reference: ruxi/make_conda_env.sh
# https://gist.github.com/ruxi/949e3d326c5a8a24ecffa8a225b2be2a 
echo This shell script recreates the conda environment 
echo for use with the xyfigure and ptg modules.

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
conda create --name $y python=3.9 black flake8 ipykernel matplotlib pytest pytest-cov scipy seaborn

# echo Activating the new $y environment...
conda init bash
conda activate $y
# 
echo Upgrading pip
python -m pip install --upgrade pip
#
# echo Finally, some pip items...
echo The pip listing prior to install...
pip list
# 
echo Installing the ptg module in developer mode...
cd ~/sibl/geo
pip install -e .
#
echo Installing the xyfigure module in developer mode...
cd ~/sibl/cli
pip install -e .
# 
echo The pip listing after install...
pip list

echo --------------------------------------------
echo The shell script setup.sh has now completed.
echo --------------------------------------------
