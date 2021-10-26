// cppmult.hpp

/*
This example from Real Python
https://realpython.com/python-bindings-overview/
https://realpython.com/python-bindings-overview/#pybind11
binds a C++ multiplication function for use in Python.
The function, cppmult, takes a an `int` and a `float` and returns a `float`.
Original source code at 
https://github.com/realpython/materials/tree/master/python-bindings
*/

#ifdef _MSC_VER
#define EXPORT_SYMBOL __declspec(dllexport)
#else
#define EXPORT_SYMBOL
#endif

#ifdef __cplusplus
extern "C"
{
    EXPORT_SYMBOL float cppmult(int int_param, float float_param);
}
#endif
