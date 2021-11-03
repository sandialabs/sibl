#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <math.h>
#include "generalpolygon.h"

#include <vector>

// pybind11 STL containers
// https: //pybind11.readthedocs.io/en/stable/advanced/cast/stl.html

// pybind11 casting between C++ and Python types
// https://pybind11.readthedocs.io/en/stable/advanced/cast/overview.html

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

int add(int a, int b)
{
    return a + b;
}

float raise_me(float base, float exponent)
{
    return pow(base, exponent);
}

struct Pet
{
    Pet(const std::string &name) : my_name(name) {}
    void setName(const std::string &name_) { my_name = name_; }
    const std::string &getName() const { return my_name; }

    std::string my_name;
};
/*
struct Parade
{
    Parade(const std::vector<float> &boundary_x, const std::vector<float> &boundary_y) : my_boundary_x(boundary_x), my_boundary_y(boundary_y) {}

    std::vector<bool> contains(const std::vector<float> &probe_x, const std::vector<float> &probe_y)
    {
        std::vector<bool> test;
        test.resize(probe_x.size(), true);
        for (unsigned int i = 0; i < my_boundary_x.size(); ++i)
            std::cout << my_boundary_x[i] << " , " << my_boundary_y[i] << std::endl;
        return test;
    }

    std::vector<float> my_boundary_x;
    std::vector<float> my_boundary_y;
};
*/
/*
struct Parade
{
    Parade(const std::vector<float> &boundary_x, const std::vector<float> &boundary_y) : GP(std::pair<std::vector<float> , std::vector<float> > (boundary_x,boundary_y) ) {}

    std::vector<bool> contains(const std::vector<float> &probe_x, const std::vector<float> &probe_y)
    {
        std::vector<bool> test(probe_x.size(),false);
        for (unsigned int i = 0; i <test.size(); ++i)
             test[i] = GP.inpoly(probe_x[i],probe_y[i]);
        return test;
    }
    GeneralizedPolygon GP;

};
*/
struct Polygon
{
    Polygon(const std::vector<float> &boundary_x, const std::vector<float> &boundary_y) : GP(std::pair<std::vector<float>, std::vector<float> >(boundary_x, boundary_y)) {}

    std::vector<bool> contains(const std::vector<float> &probe_x, const std::vector<float> &probe_y)
    {
        std::vector<bool> test(probe_x.size(), false);
        for (unsigned int i = 0; i < test.size(); ++i)
            test[i] = GP.inpoly(probe_x[i], probe_y[i]);
        return test;
    }
    GeneralizedPolygon GP;
};

namespace py = pybind11;

// PYBIND11_MODULE(module_name, module_handle)
PYBIND11_MODULE(xybind, m)
{
    m.doc() = "xybind wraps C++ libaries for use in the SIBL PTG module"; // optional module docstring

    // m.def("cpp_function", &cppmult, "A function that multiplies two numbers.");

    // example with c++ function
    m.def("add", &add, "Add two integers.");

    // example with inline lambda c++ function
    m.def(
        "subtract", [](int a, int b)
        { return a - b; },
        "Subtract two integers.");

    // attributes
    m.attr("the_answer") = 42;
    m.attr("zero") = 0;
    py::object world = py::cast("World");
    m.attr("what") = world;

    // keyword only arguments
    m.def("exponent", &raise_me, py::kw_only(), py::arg("base"), py::arg("exponent"), "Returns base to a power.");

    // struct
    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string &>())
        .def_property("name", &Pet::getName, &Pet::setName);

    // py::class_<Parade>(m, "Parade")
    //     .def(py::init<const std::vector<float> &, const std::vector<float> &>())
    //     .def("contains", &Parade::contains, py::kw_only(), py::arg("probe_x"), py::kw_only(), py::arg("probe_y"), "Returns a vector with True or False for each element with coordinates probe_x, probe_y.");

    py::class_<Polygon>(m, "Polygon")
        .def(py::init<const std::vector<float> &, const std::vector<float> &>())
        .def("contains", &Polygon::contains, py::kw_only(), py::arg("probe_x"), py::kw_only(), py::arg("probe_y"), "Returns a vector with True or False for each element with coordinates probe_x, probe_y.");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
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
