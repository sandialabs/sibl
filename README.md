# Sandia Injury Biomechanics Laboratory (SIBL)

## Purpose

The Sandia Injury Biomechanics Laboratory analyzes injury due to blast, ballistics, and blunt trauma to help the nation protect the U.S. warfighter. Our contributions to the science of injury causation and prevention aim to significantly reduce the U.S. warfighter's exposure to serious, severe, and fatal injuries.

For more information, see our [website](https://www.sandia.gov/biomechanics/).

## Library 

* Information 
  * [![python](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/) [![license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/sandialabs/sibl#license) [![pypi](https://img.shields.io/badge/pypi-v0.0.6-brightgreen.svg)](https://pypi.org/project/xyfigure/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
* Testing 
  * [![unittest](https://github.com/sandialabs/sibl/workflows/unittest/badge.svg)](https://github.com/sandialabs/sibl/actions) [![blacktest](https://github.com/sandialabs/sibl/workflows/blacktest/badge.svg)](https://github.com/sandialabs/sibl/actions) [![covertest](https://github.com/sandialabs/sibl/workflows/covertest/badge.svg)](https://github.com/sandialabs/sibl/actions) [![codecov](https://codecov.io/gh/sandialabs/sibl/branch/master/graph/badge.svg)](https://codecov.io/gh/sandialabs/sibl)
* Documentation
  * [xyfigure](xyfigure/doc/README.md)
  * [tpav](xyfigure/process/tpav/README.md)

## Workflow Choice

There are two workflows: User and Developer

 []() | **User** | **Developer**
---|---|---
Use Case | *"I just want to use the library, I don't want to develop the library."* | *"I want to use the library and develop the library."*
Configuration | First, complete the [user configuration](config/environment.md#user-configuration). | First, complete the [developer configuration](config/environment.md#developer-configuration).
Use | Then, proceed to the [documentation](xyfigure/doc/README.md).  | Then, follow the [Developer Workflow](#developer-workflow).

## Developer Workflow

```bash
# ----
# sync
# ----
$ (base) [~]$ cd ~/sibl
$ (base) [~/sibl] git status
$ (base) [~/sibl] git pull
$ (base) [~/sibl] git add, git commit -m "message", git push
#
# ---------
# implement
# ---------
$ (base) [~/sibl]$ conda activate siblenv
$ (siblenv) [~/sibl]$ # development
#
# --------
# unittest
# --------
# check unit tests (soon-to-be-standard with pytest)
$ (siblenv) [~/sibl]$ pytest # unit tests must pass prior to push to repository
$ (siblenv) [~/sibl]$ pytest -v # for more verbose unittest output
#
# check unit tests (soon-to-be-deprecated with unittest)
$ (siblenv) [~/sibl]$ python -m unittest # unit tests must pass prior to push to repository
$ (siblenv) [~/sibl]$ python -m unittest -v # for more verbose unittest output
#
# ---------
# blacktest
# ---------
$ (siblenv) [~/sibl] black --check .
#
# or to check specific folders one at a time
$ (siblenv) [~/sibl] black --check xyfigure/
$ (siblenv) [~/sibl] black --check geo/
#
# if above check failse, the diff or fix 
# diff: (without automatic code modification)
$ (siblenv) [~/sibl] black --check some_specific_file.py --diff 
$ (siblenv) [~/sibl] black --check some_folder/ --diff
# fix: (with automatic code modification)
$ (siblenv) [~/sibl] black some_specific_file.py
$ (siblenv) [~/sibl] black some_folder/
$ (siblenv) [~/sibl]
#
# ---------
# covertest
# ---------
$ (siblenv) [~/sibl]$ pytest --cov=.
#
# or to test specific folders
$ (siblenv) [~/sibl]$ pytest --cov=geo/src/ptg --cov=xyfigure/code
#
# and to add missing coverage line number reporting
$ (siblenv) [~/sibl]$ pytest --cov=geo/src/ptg --cov=xyfigure/code --cov-report term-missing
```

## Contact

* Chad B. Hovey, Sandia National Laboratories, chovey@sandia.gov

## License

* [License](LICENSE)
* [Third-Party Notice](NOTICE.md)

Sandia National Laboratories is a multimission laboratory managed and operated by National Technology and Engineering Solutions of Sandia, LLC, a wholly owned subsidiary of Honeywell International, Inc., for the U.S. Department of Energy's National Nuclear Security Administration under contract DE-NA-0003525.

## Copyright

Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains certain rights in this software.

### Notice

For five (5) years from  the United States Government is granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable worldwide license in this data to reproduce, prepare derivative works, and perform publicly and display publicly, by or on behalf of the Government. There is provision for the possible extension of the term of this license. Subsequent to that period or any extension granted, the United States Government is granted for itself and others acting on its behalf a paid-up, nonexclusive, irrevocable worldwide license in this data to reproduce, prepare derivative works, distribute copies to the public, perform publicly and display publicly, and to permit others to do so. The specific term of the license can be identified by inquiry made to National Technology and Engineering Solutions of Sandia, LLC or DOE.
 
NEITHER THE UNITED STATES GOVERNMENT, NOR THE UNITED STATES DEPARTMENT OF ENERGY, NOR NATIONAL TECHNOLOGY AND ENGINEERING SOLUTIONS OF SANDIA, LLC, NOR ANY OF THEIR EMPLOYEES, MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES ANY LEGAL RESPONSIBILITY FOR THE ACCURACY, COMPLETENESS, OR USEFULNESS OF ANY INFORMATION, APPARATUS, PRODUCT, OR PROCESS DISCLOSED, OR REPRESENTS THAT ITS USE WOULD NOT INFRINGE PRIVATELY OWNED RIGHTS.
 
Any licensee of this software has the obligation and responsibility to abide by the applicable export control laws, regulations, and general prohibitions relating to the export of technical data. Failure to obtain an export control license or other authority from the Government may result in criminal liability under U.S. laws.
