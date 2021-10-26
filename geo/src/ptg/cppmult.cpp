// cppmult.cpp

/*
This example from Real Python
https://realpython.com/python-bindings-overview/
https://realpython.com/python-bindings-overview/#pybind11
binds a C++ multiplication function for use in Python.
The function, cppmult, takes a an `int` and a `float` and returns a `float`.
Original source code at 
https://github.com/realpython/materials/tree/master/python-bindings
*/

#include <iostream>
#include <iomanip>
#include "cppmult.hpp"

float cppmult(int int_param, float float_param)
{
    float return_value = int_param * float_param;
    std::cout << std::setprecision(1) << std::fixed
              << "    In cppmult: int " << int_param
              << " float " << float_param
              << " returning " << return_value
              << std::endl;
    return return_value;
}
