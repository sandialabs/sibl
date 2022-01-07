# Sandia Injury Biomechanics Laboratory (SIBL)

## Purpose

The Sandia Injury Biomechanics Laboratory analyzes injury due to blast, ballistics, and blunt trauma to help the nation protect the U.S. warfighter. Our contributions to the science of injury causation and prevention aim to significantly reduce the U.S. warfighter's exposure to serious, severe, and fatal injuries.

For more information &mdash; including publications, presentations, and reports &mdash; see our [website](https://www.sandia.gov/biomechanics/).

## Library

The `xyfigure` library is an open-source geometry and mesh engine written in Python and C++.

### Information

[![python](https://img.shields.io/badge/python-3.9.5-blue.svg)](https://www.python.org/) 
![os](https://img.shields.io/badge/os-ubuntu%20|%20macos%20|%20windows-blue.svg)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/sandialabs/sibl#license) 
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Testing

[![pytest](https://github.com/sandialabs/sibl/workflows/pytest/badge.svg)](https://github.com/sandialabs/sibl/actions) [![blacktest](https://github.com/sandialabs/sibl/workflows/blacktest/badge.svg)](https://github.com/sandialabs/sibl/actions) [![covertest](https://github.com/sandialabs/sibl/workflows/covertest/badge.svg)](https://github.com/sandialabs/sibl/actions) [![codecov](https://codecov.io/gh/sandialabs/sibl/branch/master/graph/badge.svg)](https://codecov.io/gh/sandialabs/sibl)

### Geometry Engine

![geo_doc_fig](geo/doc/fig/N_p=2_NCP=8.png)

The *SIBL Geometry Engine* is Python library that creates Bézier and B-spline curves, surfaces, and volumes.

The mathematical development used in the library is contained in two documents:

* [Bézier Geometry](geo/doc/bezier/Bezier-Geometry-2021-12-15.pdf), and
* [B-Spline Geometry](geo/doc/bspline/B-Spline-Geometry-2021-12-15.pdf).

The examples and validations presented in the documents are all created with the *SIBL Geometry Engine*, connecting theory with implementation.  The *Geometry Engine* is a fundamental part of the Pixel to Mesh and Pixel to Geometry (PTM/PTG) [workflows](geo/doc/unit-test-ptm.md).

### Mesh Engine

![circle_boundary_mesh](geo/doc/dual/fig/circle_boundary_mesh.png)

The *SIBL Mesh Engine* is a C++ library with Python bindings that creates 2D dualized quadrilateral meshes.  Follow the [Lessons](geo/doc/dual/lesson_01.md) to get started.

### Additional Documentation

* Also see the [xyfigure](cli/doc/README.md) and [tpav](cli/tests/tpav/README.md) documentation.

### Contributing

* To get started, developers should [configure](config/README.md) their development environment.
* Then, developers should follow the developer [workflow](config/workflow.md).
* To contribute, developers should submit a merge request.

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
