# Gena

We will use `Gena` as a short name for *Generalized Adaptive Refinement for
Grid-based Hexahedral Meshing*, the title of the repository reviewed here.

## Overview

The **goal** of this document is to record the steps required to get 
[CinoLib](https://github.com/mlivesu/cinolib), created by Livesu and 
contributors, installed and running as a **local user workflow** to produce 
a hexahedral mesh from a surface representation.  This workflow requires the 
[Gen-Adapt-Ref-for-Hexmeshing repository](https://github.com/cg3hci/Gen-Adapt-Ref-for-Hexmeshing).

The specific example will be the duck model shown in the figure below 
(originally created in, and reproduced from 
[Livesu 2021b](references.md#livesu-2021b)).

![duck](fig/Livesu_2021_dual_fig_1.png)
> *Figure 0.1:  Reproduction from Fig. 1 of [Livesu 2021b](references.md#livesu-2021b).*

[References](references.md)

## Preconditions

### cmake

The `cmake` application must already be present.
Test for an existing installation:

```bash
(base) cbh@atlas ~ % which cmake
                      # <-- nothing is returned here
```

If the result from the above-stated command returns nothing, then
install `cmake` either with a [CMake installer](https://cmake.org/download/) 
or with the [Homebrew](https://brew.sh/) package manager as follows:

```bash
(base) cbh@atlas ~ % brew install cmake
```

After `cmake` is installed, the `which cmake` command will report something
similar to

```bash
(base) cbh@atlas ~ % which cmake
/opt/homebrew/bin/cmake
```

### Gurobi for (Integer Linear Programming) ILP resolution

We will use *Gurobi for Academics and Researchers*, with a 
named-user academic license.  Per 
[Academic Program and Licenses](https://www.gurobi.com/academia/academic-program-and-licenses/):

> The license can be set up on a single physical machine. Users may install and license Gurobi for their own use on more than one machine.

* [Register](https://pages.gurobi.com/registration).
* Log in.
* From the [Gurobi Optimizer page](https://www.gurobi.com/downloads), download the version for the target machine OS, and review the README.txt.
  * Download Gurobi Optimizer
    * gurobi9.5.1_macos_universal2.pkg (84.2 MB)
    * `~ % md5 ~/Downloads/gurobi9.5.1_macos_universal2.pkg`
    * md5 checksum: a1786849ff3f14041af102a3fe3c8ad1
* After downloading, visit the [Free Academic License page](https://www.gurobi.com/downloads/end-user-license-agreement-academic/) to request the free license.

The above installation will install `grbgetkey`

```bash
(base) cbh@atlas gurobi % which grbgetkey
/usr/local/bin/grbgetkey
```

### CGAL for computation of the Shape Diameter Function (SDF)

```bash
(base) cbh@atlas ~ % brew install cgal
Running `brew update --preinstall`...
==> Auto-updated Homebrew!
Updated 3 taps (homebrew/core, homebrew/cask and homebrew/cask-fonts).
==> New Formulae
epinio                   fourmolu                 ltex-ls                  nickel                   rslint                   stylish-haskell
==> Updated Formulae
Updated 424 formulae.
==> Deleted Formulae
gstreamermm
==> New Casks
abbyy-finereader-pdf          mediahuman-audio-converter    paragon-camptune              roonbridge                    rwts-pdfwriter
==> Updated Casks
Updated 201 casks.
==> Deleted Casks
finereader

==> Downloading https://ghcr.io/v2/homebrew/core/icu4c/manifests/70.1
######################################################################## 100.0%
==> Downloading https://ghcr.io/v2/homebrew/core/icu4c/blobs/sha256:43cf787a35559b90597db8e1aaba95dbeedb84b1ee3d2e942be8938ae618724c
==> Downloading from https://pkg-containers.githubusercontent.com/ghcr1/blobs/sha256:43cf787a35559b90597db8e1aaba95dbeedb84b1ee3d2e942be8938ae618724c?
######################################################################## 100.0%
==> Downloading https://ghcr.io/v2/homebrew/core/boost/manifests/1.78.0_1
######################################################################## 100.0%
==> Downloading https://ghcr.io/v2/homebrew/core/boost/blobs/sha256:8962db038baeee22886c3fccf32a73dbc117bf0098e1d576e3265e5b6d3b0545
==> Downloading from https://pkg-containers.githubusercontent.com/ghcr1/blobs/sha256:8962db038baeee22886c3fccf32a73dbc117bf0098e1d576e3265e5b6d3b0545?
######################################################################## 100.0%
==> Downloading https://ghcr.io/v2/homebrew/core/eigen/manifests/3.4.0_1
######################################################################## 100.0%
==> Downloading https://ghcr.io/v2/homebrew/core/eigen/blobs/sha256:211fd7f1d58b383e3d64335c08a376a7d8433007ce61410ead0320df34b6f4bd
==> Downloading from https://pkg-containers.githubusercontent.com/ghcr1/blobs/sha256:211fd7f1d58b383e3d64335c08a376a7d8433007ce61410ead0320df34b6f4bd?
######################################################################## 100.0%
==> Downloading https://ghcr.io/v2/homebrew/core/gmp/manifests/6.2.1_1
######################################################################## 100.0%
==> Downloading https://ghcr.io/v2/homebrew/core/gmp/blobs/sha256:a43a2ae4c44d90626b835a968a32327c8b8bbf754ec1d2590f8ac656c71dace9
==> Downloading from https://pkg-containers.githubusercontent.com/ghcr1/blobs/sha256:a43a2ae4c44d90626b835a968a32327c8b8bbf754ec1d2590f8ac656c71dace9?
######################################################################## 100.0%
==> Downloading https://ghcr.io/v2/homebrew/core/mpfr/manifests/4.1.0
######################################################################## 100.0%
==> Downloading https://ghcr.io/v2/homebrew/core/mpfr/blobs/sha256:81ced499f237acfc2773711a3f8aa985572eaab2344a70485c06f72405e4a5e7
==> Downloading from https://pkg-containers.githubusercontent.com/ghcr1/blobs/sha256:81ced499f237acfc2773711a3f8aa985572eaab2344a70485c06f72405e4a5e7?
######################################################################## 100.0%
==> Downloading https://ghcr.io/v2/homebrew/core/cgal/manifests/5.4
######################################################################## 100.0%
==> Downloading https://ghcr.io/v2/homebrew/core/cgal/blobs/sha256:cf7ee43bd5a7bf1dc2ad90ad9d3609e4cef91555870d5608621ee5ac7a32c0b0
==> Downloading from https://pkg-containers.githubusercontent.com/ghcr1/blobs/sha256:cf7ee43bd5a7bf1dc2ad90ad9d3609e4cef91555870d5608621ee5ac7a32c0b0?
######################################################################## 100.0%
==> Installing dependencies for cgal: icu4c, boost, eigen, gmp and mpfr
==> Installing cgal dependency: icu4c
==> Pouring icu4c--70.1.arm64_monterey.bottle.tar.gz
🍺  /opt/homebrew/Cellar/icu4c/70.1: 261 files, 74.9MB
==> Installing cgal dependency: boost
==> Pouring boost--1.78.0_1.arm64_monterey.bottle.tar.gz
🍺  /opt/homebrew/Cellar/boost/1.78.0_1: 15,400 files, 462.7MB
==> Installing cgal dependency: eigen
==> Pouring eigen--3.4.0_1.all.bottle.tar.gz
🍺  /opt/homebrew/Cellar/eigen/3.4.0_1: 546 files, 8.4MB
==> Installing cgal dependency: gmp
==> Pouring gmp--6.2.1_1.arm64_monterey.bottle.tar.gz
🍺  /opt/homebrew/Cellar/gmp/6.2.1_1: 21 files, 3.2MB
==> Installing cgal dependency: mpfr
==> Pouring mpfr--4.1.0.arm64_monterey.bottle.tar.gz
🍺  /opt/homebrew/Cellar/mpfr/4.1.0: 30 files, 5.2MB
==> Installing cgal
==> Pouring cgal--5.4.arm64_monterey.bottle.tar.gz
🍺  /opt/homebrew/Cellar/cgal/5.4: 3,660 files, 38.2MB
==> Running `brew cleanup cgal`...
Disable this behaviour by setting HOMEBREW_NO_INSTALL_CLEANUP.
Hide these hints with HOMEBREW_NO_ENV_HINTS (see `man brew`).
(base) cbh@atlas ~ %
```

## Getting Started

Clone the main repository with the `cinolib` submodule 
too (using the `--recursive` flag; `cinolib` itself also 
uses submodules for `eigen` and `graph_cut`):

```bash
(base) cbh@atlas ~ % git clone --recursive https://github.com/cg3hci/Gen-Adapt-Ref-for-Hexmeshing.git
Cloning into 'Gen-Adapt-Ref-for-Hexmeshing'...
remote: Enumerating objects: 97, done.
remote: Counting objects: 100% (97/97), done.
remote: Compressing objects: 100% (62/62), done.
remote: Total 97 (delta 50), reused 56 (delta 28), pack-reused 0
Receiving objects: 100% (97/97), 2.77 MiB | 4.32 MiB/s, done.
Resolving deltas: 100% (50/50), done.
Submodule 'external/Cinolib' (https://github.com/mlivesu/cinolib.git) registered for path 'external/Cinolib'
Cloning into '/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib'...
remote: Enumerating objects: 20173, done.
remote: Counting objects: 100% (5308/5308), done.
remote: Compressing objects: 100% (3322/3322), done.
remote: Total 20173 (delta 2426), reused 4199 (delta 1522), pack-reused 14865
Receiving objects: 100% (20173/20173), 27.36 MiB | 2.64 MiB/s, done.
Resolving deltas: 100% (13230/13230), done.
Submodule path 'external/Cinolib': checked out '384e6a8fd45fa3a2a5e52cd22ade154f6f0b8d10'
Submodule 'eigen' (https://gitlab.com/libeigen/eigen.git) registered for path 'external/Cinolib/external/eigen'
Submodule 'external/graph_cut' (https://github.com/mlivesu/GraphCuts) registered for path 'external/Cinolib/external/graph_cut'
Cloning into '/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib/external/eigen'...
remote: Enumerating objects: 115441, done.
remote: Counting objects: 100% (508/508), done.
remote: Compressing objects: 100% (252/252), done.
remote: Total 115441 (delta 264), reused 319 (delta 256), pack-reused 114933
Receiving objects: 100% (115441/115441), 102.85 MiB | 13.84 MiB/s, done.
Resolving deltas: 100% (95073/95073), done.
Cloning into '/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib/external/graph_cut'...
remote: Enumerating objects: 31, done.
remote: Total 31 (delta 0), reused 0 (delta 0), pack-reused 31
Receiving objects: 100% (31/31), 49.39 KiB | 754.00 KiB/s, done.
Resolving deltas: 100% (10/10), done.
Submodule path 'external/Cinolib/external/eigen': checked out '1fd5ce1002a6f30e1169b529b291216a18be2f7e'
Submodule path 'external/Cinolib/external/graph_cut': checked out '66376566852b704a0e57bf49dcac74ee5210ff18'
(base) cbh@atlas ~ %
```

Update the `FindGUROBI.cmake` file, as [indicated](https://github.com/cg3hci/Gen-Adapt-Ref-for-Hexmeshing#dependencies):

> WARNING: `FindGUROBI.cmake` is configured to search for gurobi 9.1.x versions. Please edit the "gurobi91" entry in `FindGUROBI.cmake` if you have a different gurobi version installed on your machine.




