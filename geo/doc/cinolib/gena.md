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

Install the license key (specific details omitted here).

For macOS, the installer will, by default, place the Gurobi 9.5.1 files in 
`/Library/gurobi951/macos_universal2` (note that this is the 
system `/Library` directory, not your 
personal `~/Library directory`). Your `<installdir>` 
(which we'll refer to throughout this document) will be 
`/Library/gurobi951/macos_universal2`.

```bash
(base) cbh@atlas macos_universal2 % cd /Library/gurobi951/macos_universal2
(base) cbh@atlas macos_universal2 % ll
total 424
drwxrwxr-x  13 root  admin     416 Feb 11 08:54 .
drwxrwxr-x   3 root  admin      96 Feb 11 08:14 ..
drwxrwxr-x  10 root  admin     320 Feb 11 08:55 bin
drwxrwxr-x   5 root  admin     160 Feb 11 08:14 include
drwxrwxr-x   4 root  admin     128 Feb 11 08:14 R
drwxrwxr-x  16 root  admin     512 Mar 22 13:49 docs
-rwxrwxr-x   1 root  admin    3054 Feb 11 08:14 setup.py
drwxrwxr-x  19 root  admin     608 Feb 11 08:56 matlab
drwxrwxr-x  12 root  admin     384 Feb 11 08:14 examples
-rwxrwxr-x   1 root  admin  200641 Feb 11 08:54 EULA.pdf
drwxrwxr-x  17 root  admin     544 Feb 11 08:56 lib
-rwxrwxr-x   1 root  admin   11769 Feb 11 08:54 ReleaseNotes.html
drwxrwxr-x   5 root  admin     160 Feb 11 08:14 src
```

From [Gurobi Installation Guide: macOS](https://youtu.be/ZcL-NmckTxQ) at
3:20 / 4:03.  Test the installation by running the Python interactive shell:

```bash
(base) cbh@atlas ~ % gurobi.sh
Python 3.9.2 (default, Mar 22 2021, 02:01:25)
[Clang 12.0.0 (clang-1200.0.32.29)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
Set parameter Username
Set parameter LogFile to value "gurobi.log"
Academic license - for non-commercial use only - expires 2022-05-20

Gurobi Interactive Shell (mac64), Version 9.5.1
Copyright (c) 2022, Gurobi Optimization, LLC
Type "help()" for help

gurobi>
```

If the interactive shell opens as above, then installation of Gurobi was 
successful.

The Gurobi Optimizer `readme.txt` follows:

```txt

Your first step in using version 9.5.1 of the Gurobi Optimizer is to
download the appropriate distribution for your platform:

 Gurobi-9.5.1-win64.msi:           64-bit Windows installer
 gurobi9.5.1_linux64.tar.gz:       64-bit Linux distribution
 gurobi9.5.1_macos_universal2.pkg: 64-bit universal2 macOS distribution (M1 or Intel)
 gurobi9.5.1_power64.tar.gz:       64-bit AIX distribution

If you have installed a previous version of the Gurobi Optimizer, we
recommend that you uninstall it before installing this version.

For Windows and Mac users, you can simply double-click on the
installer once you have downloaded it.  It will guide you through the
installation process.

For Linux and AIX users, you will first need to choose an install
location (w recommend /opt for a shared installation).  You can then
copy the Gurobi distribution to that location and do a 'tar xvfz
gurobi9.5.1_linux64.tar.gz' (e.g.) to extract the Gurobi files.
Please check our supported platform list (in the Release Notes or on
our web site) to make sure that your operating system is supported.

Once the Gurobi files have been installed, your next step is to
consult the Release Notes and the Gurobi Quick Start guide.  The
Release Notes are accessible from the following locations:

Windows: c:\gurobi951\win64\ReleaseNotes.html
Linux: /opt/gurobi951/linux64/ReleaseNotes.html
Mac universal2: /Library/gurobi951/macos_universal2/ReleaseNotes.html
AIX: /opt/gurobi951/power64/ReleaseNotes.html

The Quick Start Guide provides instructions for obtaining and installing
your Gurobi Optimizer license.  The Release Notes contain information about
this release, as well as a link to the Quick Start Guide.

If you already have a Gurobi Version 9 license (in file 'gurobi.lic'),
and you would like to store it in the default location, you should
copy the file to c:/gurobi951 on Windows, /opt/gurobi951 on Linux or
AIX, or /Library/gurobi951 on Mac.

Note that, due to limited Python support on AIX, our AIX port does not
include the Interactive Shell or the Python interface.  We also don't
provide an R interface on AIX.
```

[Release notes](https://cdn.gurobi.com/wp-content/uploads/2022/03/release-notes-9_5_1.html)


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

```bash
(base) cbh@atlas ~ % cd Gen-Adapt-Ref-for-Hexmeshing
(base) cbh@atlas ~ % nvim FindGUROBI.cmake
```

The `FindGUROBI.cmake` line 7 update, from:

```cmake
    NAMES gurobi gurobi91
```

to

```cmake
    NAMES gurobi gurobi95
```

Compile

```bash
(base) cbh@atlas Gen-Adapt-Ref-for-Hexmeshing % mkdir build; cd build
(base) cbh@atlas build % cmake -DCMAKE_BUILD_TYPE=Release ..
CMake Warning (dev) at CMakeLists.txt:25:
  Syntax Warning in cmake code at column 27

  Argument not separated from preceding token by whitespace.
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at CMakeLists.txt:26:
  Syntax Warning in cmake code at column 24

  Argument not separated from preceding token by whitespace.
This warning is for project developers.  Use -Wno-dev to suppress it.

-- The C compiler identification is AppleClang 13.1.6.13160021
-- The CXX compiler identification is AppleClang 13.1.6.13160021
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /Library/Developer/CommandLieTools/usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /Library/Developer/CommandLineTools/usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
CMake Warning at /opt/homebrew/lib/cmake/CGAL/CGALConfig.cmake:92 (message):
  CGAL_DATA_DIR cannot be deduced, set the variable CGAL_DATA_DIR to set the
  default value of CGAL::data_file_path()
Call Stack (most recent call first):
  CMakeLists.txt:20 (find_package)


-- Using header-only CGAL
-- Targetting Unix Makefiles
-- Using /Library/Developer/CommandLineTools/usr/bin/c++ compiler.
-- DARWIN_VERSION=21
-- Mac Leopard detected
-- Found GMP: /opt/homebrew/lib/libgmp.dylib
-- Found MPFR: /opt/homebrew/lib/libmpfr.dylib
-- Found Boost: /opt/homebrew/lib/cmake/Boost-1.78.0/BoostConfig.cmake (found suitable version "1.78.0", minimum required is "1.48")
-- Boost include dirs: /opt/homebrew/include
-- Boost libraries:
-- Looking for pthread.h
-- Looking for pthread.h - found
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Success
-- Found Threads: TRUE
-- Found GUROBI: /usr/local/lib/libgurobi95.dylib
BUILD_TYPE: Release
GUROBI_HOME:
GUROBI_INCLUDE: GUROBI_INCLUDE_DIRS-NOTFOUND
GUROBI_LIBS: /usr/local/lib/libgurobi95.dylib GUROBI_CXX_LIBRARY-NOTFOUND
-- Configuring done
CMake Error: The following variables are used in this project, but they are set to NOTFOUND.
Please set them or make sure they are set and tested correctly in the CMake files:
/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/GUROBI_INCLUDE_DIRS
   used as include directory in directory /Users/cbh/Gen-Adapt-Ref-for-Hexmeshing
GUROBI_CXX_LIBRARY
    linked by target "make_grid" in directory /Users/cbh/Gen-Adapt-Ref-for-Hexmeshing

-- Generating done
CMake Generate step failed.  Build files cannot be regenerated correctly.
(base) cbh@atlas build %n
```

Try to specify the `/Library/gurobi951/macos_universal2` location:

```bash
(base) cbh@atlas build % cmake .. -DCMAKE_BUILD_TYPE=Release -DGUROBI_HOME=/Library/gurobi951/macos_universal2
```

didn't work either.  Needed to set an environment variable:

```bash
(base) cbh@atlas zsh % pwd
/Users/cbh/.config/zsh
(base) cbh@atlas zsh % nvim .zshrc_atlas
```

And add to the `.zsrch_atlas` file:

```bash
# set an environment variable for gurobi 2022-03-22
export GUROBI_HOME=/Library/gurobi951/macos_universal2
```

Confirm `~/.zsrhc` sources the `atlas` machine local file:

```bash
# /bin/zsh $HOME/.config/zsh/.zshrc_atlas
source $HOME/.config/zsh/.zshrc_atlas
```

Finally

```bash
(base) cbh@atlas ~ % cd ~
(base) cbh@atlas ~ % source .zshrc
--------------------
This is .zshrc_atlas
--------------------
---------------------
This is .zshrc_global
---------------------
Setting cbh command line interface shortcuts

```

Confirm the environment variable:

```bash
(base) cbh@atlas ~ % env
# ...
GUROBI_HOME=/Library/gurobi951/macos_universal2
_=/usr/bin/env
(base) cbh@atlas ~ %
```

Now do `cmake` and `make`:

```bash
(base) cbh@atlas ~ % cd ~/Gen-Adapt-Ref-for-Hexmeshing/build

(base) cbh@atlas build % cmake .. -DCMAKE_BUILD_TYPE=Release
CMake Warning (dev) at CMakeLists.txt:25:
  Syntax Warning in cmake code at column 27

  Argument not separated from preceding token by whitespace.
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning (dev) at CMakeLists.txt:26:
  Syntax Warning in cmake code at column 24

  Argument not separated from preceding token by whitespace.
This warning is for project developers.  Use -Wno-dev to suppress it.

CMake Warning at /opt/homebrew/lib/cmake/CGAL/CGALConfig.cmake:92 (message):
  CGAL_DATA_DIR cannot be deduced, set the variable CGAL_DATA_DIR to set the
  default value of CGAL::data_file_path()
Call Stack (most recent call first):
  CMakeLists.txt:20 (find_package)


-- Using header-only CGAL
-- Targetting Unix Makefiles
-- Using /Library/Developer/CommandLineTools/usr/bin/c++ compiler.
-- DARWIN_VERSION=21
-- Mac Leopard detected
-- Boost include dirs: /opt/homebrew/include
-- Boost libraries:
BUILD_TYPE: Release
GUROBI_HOME: /Library/gurobi951/macos_universal2
GUROBI_INCLUDE: /Library/gurobi951/macos_universal2/include
GUROBI_LIBS: /usr/local/lib/libgurobi95.dylib /Library/gurobi951/macos_universal2/lib/libgurobi_c++.a
-- Configuring done
-- Generating done
-- Build files have been written to: /Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/build

(base) cbh@atlas build % ll
total 64
drwxr-xr-x   6 cbh  staff    192 Mar 22 16:30 .
drwxr-xr-x  14 cbh  staff    448 Mar 22 14:23 ..
drwxr-xr-x  13 cbh  staff    416 Mar 22 16:30 CMakeFiles
-rw-r--r--   1 cbh  staff   5322 Mar 22 16:30 Makefile
-rw-r--r--   1 cbh  staff   1557 Mar 22 14:24 cmake_install.cmake
-rw-r--r--   1 cbh  staff  17411 Mar 22 16:30 CMakeCache.txt

(base) cbh@atlas build % make
[ 50%] Building CXX object CMakeFiles/make_grid.dir/main.cpp.o
In file included from /Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/main.cpp:48:
In file included from /Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/code/mesh_projection/project.h:47:
/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib/include/cinolib/grid_projector.h:46:15: warning: anonymous non-C-compatible type given name for linkage purposes by typedef declaration; add a tag name here [-Wnon-c-typedef-for-linkage]
typedef struct
              ^
               GridProjectorOptions
/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib/include/cinolib/grid_projector.h:48:26: note: type is not C-compatible due to this default member initializer
    double conv_thresh = 1e-4;  // convergence threshold (either H or mean distance from target)
                         ^~~~
/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib/include/cinolib/grid_projector.h:53:1: note: type is given name 'GridProjectorOptions' for linkage purposes by this typedef declaration
GridProjectorOptions;
^
In file included from /Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/main.cpp:48:
In file included from /Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/code/mesh_projection/project.h:48:
/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib/include/cinolib/feature_network.h:53:15: warning: anonymous non-C-compatible type given name for linkage purposes by typedef declaration; add a tag name here [-Wnon-c-typedef-for-linkage]
typedef struct
              ^
               FeatureNetworkOptions
/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib/include/cinolib/feature_network.h:55:50: note: type is not C-compatible due to this default member initializer
    bool  split_lines_at_high_curvature_points = true;
                                                 ^~~~
/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib/include/cinolib/feature_network.h:58:1: note: type is given name 'FeatureNetworkOptions' for linkage purposes by this typedef declaration
FeatureNetworkOptions;
^
In file included from /Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/main.cpp:48:
In file included from /Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/code/mesh_projection/project.h:52:
/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib/include/cinolib/smoother.h:92:15: warning: anonymous non-C-compatible type given name for linkage purposes by typedef declaration; add a tag name here [-Wnon-c-typedef-for-linkage]
typedef struct
              ^
               SmootherOptions
/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib/include/cinolib/smoother.h:94:34: note: type is not C-compatible due to this default member initializer
    uint   n_iters             = 1;       // # of smoothing iterations
                                 ^
/Users/cbh/Gen-Adapt-Ref-for-Hexmeshing/external/Cinolib/include/cinolib/smoother.h:103:1: note: type is given name 'SmootherOptions' for linkage purposes by this typedef declaration
SmootherOptions;
^
3 warnings generated.
[100%] Linking CXX executable make_grid
[100%] Built target make_grid
(base) cbh@atlas build % ll
total 3520
drwxr-xr-x   7 cbh  staff      224 Mar 22 16:31 .
drwxr-xr-x  14 cbh  staff      448 Mar 22 14:23 ..
-rwxr-xr-x   1 cbh  staff  1768758 Mar 22 16:31 make_grid
drwxr-xr-x  13 cbh  staff      416 Mar 22 16:31 CMakeFiles
-rw-r--r--   1 cbh  staff     5322 Mar 22 16:30 Makefile
-rw-r--r--   1 cbh  staff     1557 Mar 22 14:24 cmake_install.cmake
-rw-r--r--   1 cbh  staff    17411 Mar 22 16:30 CMakeCache.txt
(base) cbh@atlas build % ./make_grid --help
usage: ./grid_maker (--surface | --polycube) --input_mesh_path=MESH_PATH --output_grid_path=GRID_PATH [Options]
Options:
--input_pc_mesh_path=PATH (required for polycube pipeline). Specify the path of the polycube map
--min_refinement=VALUE (optional, default 0[5 for polycube])
--max_refinement=VALUE (optional, default 8)
--use_octree (optional). Use the algorithmic pairing process (for surface pipeline only)
--weak_balancing | --strong_balancing (optional, default weak_balancing)
--sanity_check=BOOL (optional, default true). Test if the final mesh is paired correctly
--install_schemes=BOOL (optional, default false). Install the transition schemes to get a conforming all-hexa grid
--project_mesh=BOOL (optional, default false). Project the grid on the target mesh
(base) cbh@atlas build %
```

