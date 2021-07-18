# cinolib

  * [Install](#install)
  * [Run](#run)

## Install

### *2021-07-10* 

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

* See the [internal Qt page](qt.md) to install cinlab's dependencies on Qt.

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

The original `01_base_app_trimesh.pro` file:

```bash

TEMPLATE        = app
TARGET          = $$PWD/../01_base_app_trimesh_demo
QT             += core opengl
CONFIG         += c++11 release
CONFIG         -= app_bundle
INCLUDEPATH    += $$PWD/../../external/eigen
INCLUDEPATH    += $$PWD/../../include
DEFINES        += CINOLIB_USES_OPENGL
DEFINES        += CINOLIB_USES_QT
QMAKE_CXXFLAGS += -Wno-deprecated-declarations # gluQuadric gluSphere and gluCylinde are deprecated in macOS 10.9
DATA_PATH       = \\\"$$PWD/../data/\\\"
DEFINES        += DATA_PATH=$$DATA_PATH
SOURCES        += main.cpp

# just for Linux
unix:!macx {
DEFINES += GL_GLEXT_PROTOTYPES
LIBS    += -lGLU
}
```

### *2021-07-11*

From the [QApplication](https://doc.qt.io/qt-6/qapplication.html) class docs, `qmake` must include `+=widgets`, so update the `01_base_app_trimesh.pro` `QT` line to be

```bash
QT             += core opengl widgets
```

Great!  Now we pass the `<QApplication>` error, but get this `<QGLWidget>` error:

```bash
/Users/sparta/cinolib/include/cinolib/textures/textures.cpp:55: error: 'QGLWidget' file not found
In file included from ../01_base_app_trimesh/main.cpp:13:
In file included from ../../include/cinolib/meshes/meshes.h:43:
In file included from ../../include/cinolib/meshes/drawable_trimesh.h:42:
In file included from ../../include/cinolib/meshes/abstract_drawable_polygonmesh.h:43:
In file included from ../../include/cinolib/gl/draw_lines_tris.h:54:
In file included from ../../include/cinolib/textures/textures.h:141:
../../include/cinolib/textures/textures.cpp:55:10: fatal error: 'QGLWidget' file not found
#include <QGLWidget>
         ^~~~~~~~~~~
```

The `QGLWidget` does not appear in the Qt 6 documentation, but it does appear in the Qt 5.15 documentation [here](https://doc.qt.io/qt-5/qglwidget.html), and from [this](https://doc.qt.io/qt-6/opengl-changes-qt6.html)

Within `textures.cpp` which `#include <QGLWidget>`, line 230 shows `QImage img = QGLWidget::convertToGLFormat(QImage(bitmap));`, with Qt [doc](https://doc.qt.io/qt-5/qglwidget.html#convertToGLFormat).
Who might provide `convertToGLFormat` in Qt 6?

* Think easier path is to uninstall Qt 6 (version 6.1.2, and version 6.1.1 was just recently released on 2021-06-07, see [note](https://www.qt.io/blog/qt-6.1.1-released)) and then install Qt 5 (version 5.15), as I think Qt compatibility with cinolib is a very large undertaking, beyond scope of current investigation.

### *2021-07-17*

Git pull to update repo, see line 45 of `glcanvas.h` has changed from `#include <QOpenGLWidget>` to `#include <QGLWidget>`.  This is due to a local change that I did.  

Delete `~/cinolib/` folder and start with a fresh git clone.

```bash
> git clone --recursive git@github.com:mlivesu/cinolib.git

Cloning into 'cinolib'...
remote: Enumerating objects: 16243, done.
remote: Counting objects: 100% (1378/1378), done.
remote: Compressing objects: 100% (565/565), done.
remote: Total 16243 (delta 914), reused 1016 (delta 619), pack-reused 14865
Receiving objects: 100% (16243/16243), 22.09 MiB | 5.42 MiB/s, done.
Resolving deltas: 100% (11718/11718), done.
Submodule 'eigen' (https://gitlab.com/libeigen/eigen.git) registered for path 'external/eigen'
Submodule 'external/graph_cut' (https://github.com/mlivesu/GraphCuts) registered for path 'external/graph_cut'
Cloning into '/Users/sparta/cinolib/external/eigen'...
remote: Enumerating objects: 110406, done.
remote: Counting objects: 100% (42/42), done.
remote: Compressing objects: 100% (36/36), done.
remote: Total 110406 (delta 20), reused 17 (delta 6), pack-reused 110364
Receiving objects: 100% (110406/110406), 101.42 MiB | 11.51 MiB/s, done.
Resolving deltas: 100% (90804/90804), done.
Cloning into '/Users/sparta/cinolib/external/graph_cut'...
remote: Enumerating objects: 31, done.
remote: Total 31 (delta 0), reused 0 (delta 0), pack-reused 31
Submodule path 'external/eigen': checked out '1fd5ce1002a6f30e1169b529b291216a18be2f7e'
Submodule path 'external/graph_cut': checked out '66376566852b704a0e57bf49dcac74ee5210ff18'
⋊> ~
```

Now follow [Qt install](qt.md#2021-07-17) section.

Questions or Comments for Marco Livesu:

* [arXiv](https://arxiv.org/abs/2103.07745) paper
  * Fig 5, transition from `4x4` to `2x2`, states there are "14 hanging nodes with valence 5", but I think I count 16 hanging nodes with valence 5 (the black dots).
  