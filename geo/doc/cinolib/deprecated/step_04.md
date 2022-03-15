# Step 04: Install [CGAL](https://www.cgal.org/)

To come.

* CGAL is used for the computation of the Shape Diameter Function (SDF).

* Install `cmake`, following the [Getting Started with CMake](../cmake/README.md) document as needed.

Copy the `bunny.obj` to the local directory.

```bash
> cd ~/sibl/geo/doc/cinolib
> cp ~/cinolib/examples/data/bunny.obj .
```

Create `~/sibl/geo/doc/cinolib/CMakeLists.txt` with the following contents:

```bash
cmake_minimum_required(VERSION 3.2)
project(cinolib_demo)
add_executable(${PROJECT_NAME} main.cpp)
set(CINOLIB_USES_OPENGL_GLFW_IMGUI ON)
find_package(cinolib REQUIRED)
target_link_libraries(${PROJECT_NAME} cinolib)
```

Create a `~/sibl/geo/doc/cinolib/main.cpp` with the following contents:

```c
#include <cinolib/meshes/drawable_trimesh.h>
#include <cinolib/gl/glcanvas.h>

int main()
{
    using namespace cinolib;
    DrawableTrimesh<> m("bunny.obj");
    GLcanvas gui;
    gui.push(&m);
    return gui.launch();
}
```

Create a `build` subfolder and make the executable:

```bash
> mkdir build
> cd build/
> cmake .. -DCMAKE_BUILD_TYPE=Release -Dcinolib_DIR=/Users/chovey/cinolib
-- The C compiler identification is AppleClang 12.0.0.12000032
-- The CXX compiler identification is AppleClang 12.0.0.12000032
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
CINOLIB OPTIONAL MODULES: OpenGL, GLFW, ImGui
-- Found OpenGL: /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX11.1.sdk/System/Library/Frameworks/OpenGL.framework
-- Looking for pthread.h
-- Looking for pthread.h - found
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Success
-- Found Threads: TRUE
-- Using Cocoa for window creation
-- Configuring done
-- Generating done
-- Build files have been written to: /Users/chovey/sibl/geo/doc/cinolib/build
>
```

# Example 01: Trimesh Viewer

```bash
> cd /Users/chovey/cinolib/examples/01_trimesh_viewer
> g++ -O3 -std=c++11 -I/Users/chovey/cinolib/include/ main.cpp -o test.out
In file included from main.cpp:1:
In file included from /Users/chovey/cinolib/include/cinolib/meshes/meshes.h:40:
In file included from /Users/chovey/cinolib/include/cinolib/meshes/trimesh.h:41:
In file included from /Users/chovey/cinolib/include/cinolib/meshes/mesh_attributes.h:39:
In file included from /Users/chovey/cinolib/include/cinolib/geometry/vec_mat.h:40:
In file included from /Users/chovey/cinolib/include/cinolib/geometry/vec_mat_utils.h:136:
/Users/chovey/cinolib/include/cinolib/geometry/vec_mat_utils.cpp:42:10: fatal error: 'Eigen/Dense' file not found
#include <Eigen/Dense>
         ^~~~~~~~~~~~~
1 error generated.
chovey@s1060600 ~/c/e/01_trimesh_viewer (master) [1]>
```

# To be determined

* Locate the source code, e.g., `/Users/chovey/sibl/geo/doc/cinolib`.
* Locate the build directory, e.g., `/Users/chovey/sibl/doc/cinolib/build`.

![](fig/cmake_toy_problem.png)
> *Figure: CMake configuration for toy problem.*

[Index](README.md)

Previous: [Step 03](step_03.md)

Next: [Step nn](step_nn.md)
