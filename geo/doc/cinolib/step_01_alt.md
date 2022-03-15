# Readme

## git clone

```bash
cd ~
git clone git@github.com:mlivesu/cinolib.git
cd cinolib/examples
mkdir build
cd build
```

## cmake

```bash
# echo $USER
# sparta
# for the user user called `sparta`:

cmake .. -DCMAKE_BUILD_TYPE=Release -Dcinolib_DIR=/Users/sparta/cinolib
-- The C compiler identification is AppleClang 12.0.0.12000032
-- The CXX compiler identification is AppleClang 12.0.0.12000032
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /Library/Developer/CommandLineTools/usr/bin/cc - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /Library/Developer/CommandLineTools/usr/bin/c++ - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
CINOLIB OPTIONAL MODULES: OpenGL, GLFW, ImGui
-- Found OpenGL: /Library/Developer/CommandLineTools/SDKs/MacOSX11.0.sdk/System/Library/Frameworks/OpenGL.framework
-- Looking for pthread.h
-- Looking for pthread.h - found
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Success
-- Found Threads: TRUE
-- Using Cocoa for window creation
CINOLIB OPTIONAL MODULE: Tetgen
CINOLIB OPTIONAL MODULE: Triangle
CINOLIB OPTIONAL MODULE: Exact Predicates
CINOLIB OPTIONAL MODULE: Boost
-- Found Boost: /usr/local/lib/cmake/Boost-1.76.0/BoostConfig.cmake (found version "1.76.0")
CINOLIB OPTIONAL MODULE: VTK
CMake Warning at /Users/sparta/cinolib/cinolib-config.cmake:115 (find_package):
  By not providing "FindVTK.cmake" in CMAKE_MODULE_PATH this project has
  asked CMake to find a package configuration file provided by "VTK", but
  CMake did not find one.

  Could not find a package configuration file provided by "VTK" with any of
  the following names:

    VTKConfig.cmake
    vtk-config.cmake

  Add the installation prefix of "VTK" to CMAKE_PREFIX_PATH or set "VTK_DIR"
  to a directory containing one of the above files.  If "VTK" provides a
  separate development package or SDK, be sure it has been installed.
Call Stack (most recent call first):
  CMakeLists.txt:15 (find_package)


Could not find VTK!
-- Configuring done
-- Generating done
-- Build files have been written to: /Users/sparta/cinolib/examples/build
```

## make

```
~/cinolib/examples/build(gitmaster)✔> make
[  1%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/context.c.o
[  2%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/init.c.o
[  3%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/input.c.o
[  4%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/monitor.c.o
[  5%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/vulkan.c.o
[  6%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/window.c.o
[  7%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/cocoa_init.m.o
[  8%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/cocoa_joystick.m.o
[  9%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/cocoa_monitor.m.o
[ 10%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/cocoa_window.m.o
[ 10%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/cocoa_time.c.o
[ 11%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/posix_thread.c.o
[ 12%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/nsgl_context.m.o
[ 13%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/egl_context.c.o
[ 14%] Building C object imgui/glfw/src/CMakeFiles/glfw.dir/osmesa_context.c.o
[ 15%] Linking C static library libglfw3.a

```
