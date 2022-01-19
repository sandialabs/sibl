/*
* arrayProduct.cpp - example in MATLAB External Interfaces
*
* Multiplies an input scalar (multiplier)
* times a MxN matrix (inMatrix)
* and outputs a MxN matrix (outMatrix)
*
* Usage : from MATLAB
*         >> outMatrix = arrayProduct(multiplier, inMatrix)
*
* This is a C++ MEX-file for MATLAB.
* Copyright 2017 The MathWorks, Inc.
*
*/

#include "mex.hpp"
#include "mexAdapter.hpp"
#include <iostream>
class MexFunction : public matlab::mex::Function {
public:
    void operator()(matlab::mex::ArgumentList outputs, matlab::mex::ArgumentList inputs) {
       
        std::cout<<"Hello World"<<std::endl;
        outputs[0] = 0;
    }

    void arrayProduct(matlab::data::TypedArray<double>& inMatrix, double multiplier) {
        
        for (auto& elem : inMatrix) {
            elem *= multiplier;
        }
    }

 