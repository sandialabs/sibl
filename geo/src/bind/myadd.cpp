// myadd.cpp
#include <pybind11/pybind11.h>

int add(int a, int b)
{
    return a + b;
}

// The pybind11 module macro:
// Building pybind11 manually
// https://pybind11.readthedocs.io/en/stable/compiling.html#building-manually

/* 
From: https://github.com/pybind/pybind11/blob/1376eb0e518ff2b7b412c84a907dd1cd3f7f2dcd/include/pybind11/detail/common.h#L267

    This macro creates the entry point that will be invoked when the Python interpreter
    imports an extension module. The module name is given as the fist argument and it
    should not be in quotes. The second macro argument defines a variable of type
    `py::module` which can be used to initialize the module.
*/

namespace py = pybind11;

// PYBIND11_MODULE(module_name, module_handle)
PYBIND11_MODULE(xybind, m)
{
    m.doc() = "ptgbind wraps C++ libaries used in ptg"; // optional module docstring
    // m.def("cpp_function", &cppmult, "A function that multiplies two numbers.");
    m.def("add", &add, "Add two integers.");
}
