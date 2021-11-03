#include <pybind11/pybind11.h>

namespace py = pybind11;

int add(int i, int j)
{
    return i + j;
}

/*
void print_dict(const py::dict &dict)
{
    // C++ interacts with a Python type
    for (auto item : dict)
        std::cout << "key=" << std::string(py::str(item.first)) << ", "
                  << "value=" << std::string(py::str(item.second))
                  << std::endl;
}
*/

struct Pet
{
    Pet(const std::string &name) : my_name(name) {}
    void setName(const std::string &name_) { my_name = name_; }
    const std::string &getName() const { return my_name; }

    std::string my_name;
}

struct Dog : Pet
{
    Dog(const std::string &name) : Pet(name) {}
    std::string bark() const { return "woof!"; }
}

//PYBIND11_MODULE(xybind, m)
PYBIND11_MODULE(example, m)
{
    // basic construction
    m.doc() = "pybind11 example plugin"; // optional module string
    m.def("add", &add, "A function that adds two numbers.", py::arg("i"), py::arg("j"));

    // attributes
    m.attr("the_answer") = 42;
    m.attr("zero") = 0;
    py::object world = py::cast("World");
    m.attr("what") = world;

    // dictionary
    m.def("print_dict", &print_dict, "Prints the Python dictionary from within C++.");

    // class
    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string &>())
        .def_property("name", &Pet::getName, &Pet::setName)
        .def("__repr__", [](const Pet &a)
             { return "<example.Pet named '" + a.my_name + "'>"; });

    // specify the C++ parent type of Dog as Pet
    py::class_<Dog, Pet>(m, "Dog")
        .def(py::init<const std::string &>())
        .def("bark", &Dog::bark);
}
