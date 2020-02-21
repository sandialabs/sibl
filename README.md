# Sandia Injury Biomechanics Laboratory (SIBL)

![banner](img/blast_feature_960.jpg)

## Purpose

The Sandia Injury Biomechanics Laboratory analyzes injury due to blast, ballistics, and blunt trauma to help the nation protect the U.S. warfighter. Our contributions to the science of injury causation and prevention aim to significantly reduce the U.S. warfighter's exposure to serious, severe, and fatal injuries.

For more information, see our [website](http://www.sandia.gov/biomechanics/).

## Library [![](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-3610/) [![](https://img.shields.io/github/license/ResidentMario/missingno.svg)](https://github.com/sandialabs/sibl#license)

* XYFigure 
  * [Getting started](xyfigure/README.md)
  * [Documentation](xyfigure/XYFigure_dictionary.md)
  * [Test Cases](xyfigure/test/README.md)

## Prerequisites

* Python 3.6 or higher (the library requires f-strings)
* Scipy
* Pillow 

```console
$ python3 -m pip install Pillow
```

## Workflow

For an overview, [read the guide](https://guides.github.com/activities/hello-world/) from GitHub.

### Get a local copy of the repository using `git clone` with SSH

```console
$ cd ~  # Starting from the home directory is optional, but recommended.
$ git clone git@github.com:sandialabs/sibl.git
```

### Push to the repository

If you update the codebase, and wish to have the modifications merged into the main repository, you will need to either *push to the repository* if you are a collaborator (information below), or *create a pull request* if you have forked the repo (information to come).

In the `~/sibl/.git/config` file, add the following:

```python
[user]
    name = James Bond  # your first and last name
    email = jb007@company.com  # your email address
```

Configure ssh keys between your local and the repo.  This assumes to you have an existing public key file in `~/.ssh/id_rsa/id_rsa.pub`.  See [this](https://help.github.com/en/github/authenticating-to-github/connecting-to-github-with-ssh) to create a public key.  See [this](https://help.github.com/en/github/authenticating-to-github) for troubleshooting.

Copy the entire **public** key to the GitHub site under [Settings > SSH and GPG keys](https://github.com/settings/keys).

From within the repo `~/sibl/`, set the username and email on a *per-repo* basis:

```console
$ git config user.name "James Bond"  # your first and last name in quotations
$ git config user.email "jb007@company.com"  # your email address in quotations
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
