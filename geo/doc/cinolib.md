# cinolib

  * [Install](#install)
  * [Run](#run)

## Install

Following the cinolab [instructions](https://github.com/mlivesu/cinolib#usage),

```bash
> cd ~/
> git clone --recursive https://github.com/mlivesu/cinolib.git

Cloning into 'cinolib'...
remote: Enumerating objects: 16218, done.
remote: Counting objects: 100% (1353/1353), done.
remote: Compressing objects: 100% (545/545), done.
remote: Total 16218 (delta 900), reused 1004 (delta 616), pack-reused 14865
Receiving objects: 100% (16218/16218), 22.08 MiB | 4.74 MiB/s, done.
Resolving deltas: 100% (11704/11704), done.
Submodule 'external/eigen' (https://github.com/eigenteam/eigen-git-mirror) registered for path 'external/eigen'
Submodule 'external/graph_cut' (https://github.com/mlivesu/GraphCuts) registered for path 'external/graph_cut'
Cloning into '/Users/sparta/cinolib/external/eigen'...
remote: Enumerating objects: 103968, done.
remote: Total 103968 (delta 0), reused 0 (delta 0), pack-reused 103968
Receiving objects: 100% (103968/103968), 95.95 MiB | 5.29 MiB/s, done.
Resolving deltas: 100% (85752/85752), done.
Cloning into '/Users/sparta/cinolib/external/graph_cut'...
remote: Enumerating objects: 31, done.
remote: Total 31 (delta 0), reused 0 (delta 0), pack-reused 31
Submodule path 'external/eigen': checked out '36b95962756c1fce8e29b1f8bc45967f30773c00'
Submodule path 'external/graph_cut': checked out '66376566852b704a0e57bf49dcac74ee5210ff18'
>
```

* [Qt Creator IDE](https://www.qt.io/product) is required for the GUI.

> *Qt Creator is a cross-platform integrated development environment (IDE) built for the maximum developer experience. Qt Creator runs on Windows, Linux, and macOS desktop operating systems, and allows developers to create applications across desktop, mobile, and embedded platforms.*

* See the internal [Qt page](qt.md) to install cinlab's dependencies on Qt.

## Run

See [examples](https://github.com/mlivesu/cinolib/tree/master/examples#examples).

```bash
> cd examples/
> vim README.md
```

From Qt Creator > Compile Output tab

```bash
12:22:42: Running steps for project 01_base_app_trimesh...
12:22:42: Starting: "/Users/sparta/Qt/6.1.2/macos/bin/qmake" /Users/sparta/cinolib/examples/01_base_app_trimesh/01_base_app_trimesh.pro -spec macx-clang CONFIG+=debug CONFIG+=x86_64 CONFIG+=qml_debug
Info: creating stash file /Users/sparta/cinolib/examples/build-01_base_app_trimesh-Qt_6_1_2_for_macOS-Debug/.qmake.stash
12:22:42: The process "/Users/sparta/Qt/6.1.2/macos/bin/qmake" exited normally.
12:22:42: Starting: "/usr/bin/make" -f /Users/sparta/cinolib/examples/build-01_base_app_trimesh-Qt_6_1_2_for_macOS-Debug/Makefile qmake_all
make: Nothing to be done for `qmake_all'.
12:22:42: The process "/usr/bin/make" exited normally.
12:22:42: Starting: "/usr/bin/make" -j8
/Library/Developer/CommandLineTools/usr/bin/clang++ -c -pipe -stdlib=libc++ -Wno-deprecated-declarations -O2 -std=gnu++1z  -arch x86_64 -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk -mmacosx-version-min=10.14 -Wall -Wextra -fPIC -DCINOLIB_USES_OPENGL -DCINOLIB_USES_QT -DDATA_PATH=\"/Users/sparta/cinolib/examples/01_base_app_trimesh/../data/\" -DQT_QML_DEBUG -DQT_NO_DEBUG -DQT_OPENGL_LIB -DQT_GUI_LIB -DQT_CORE_LIB -I../01_base_app_trimesh -I. -I../../external/eigen -I../../include -I../../../Qt/6.1.2/macos/lib/QtOpenGL.framework/Headers -I../../../Qt/6.1.2/macos/lib/QtGui.framework/Headers -I../../../Qt/6.1.2/macos/lib/QtCore.framework/Headers -I. -I/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/OpenGL.framework/Headers -I/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/AGL.framework/Headers -I/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/OpenGL.framework/Headers -I/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/AGL.framework/Headers -I../../../Qt/6.1.2/macos/mkspecs/macx-clang -F/Users/sparta/Qt/6.1.2/macos/lib -o main.o ../01_base_app_trimesh/main.cpp
../01_base_app_trimesh/main.cpp:12:10: fatal error: 'QApplication' file not found
#include <QApplication>
         ^~~~~~~~~~~~~~
1 error generated.
make: *** [main.o] Error 1
12:22:44: The process "/usr/bin/make" exited with code 2.
Error while building/deploying project 01_base_app_trimesh (kit: Qt 6.1.2 for macOS)
When executing step "Make"
12:22:44: Elapsed time: 00:02.

```
