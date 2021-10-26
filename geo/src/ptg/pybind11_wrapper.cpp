// pybind11_wrapper.cpp
#include <pybind11/pybind11.h>
#include <cppmult.hpp>

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

// PYBIND11_MODULE(module_name, module_handle)
PYBIND11_MODULE(pybind11_example, m)
{
    m.doc() = "pybind11 example plugin"; // optional module docstring
    m.def("cpp_function", &cppmult, "A function that multiplies two numbers.");
}
