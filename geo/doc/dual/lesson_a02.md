# MATLAB workflow

## Goals

Use MATLAB and text file interop to run the C++ engine and post-process results.

## Prerequisites

Compile the C++ code to generate an executable. 

On a Mac or Linux machine, compile at the command line and renaming the a.out executable.
```bash 
>g++ -O3 -std=c++11 *.cpp
>mv a.out dual.out
```  

On a Windows machine you'll need to install a C++ compiler. The simplest route that has an IDE is Code::Blocks WITH MinGW. Then you'd create a console application project, add all the .cpp and .h files to the project. Under Project->Build Options you'll need to select "... follow the C++11 ISO ...". Under Build-> Select Target, pick "Release", and then Build->Build. This will generate an executable in a "bin" subfolder which you can freely move about.

## Steps

Generate an input YML file which will specify to the engine what procedures to do. For this example, use [`circle.yml`](circle.yml). Running the executable will automatically generate a template YML file that you can modify.

Open [`plotCircleEx.m`](plotCircleEx.m)In Matlab editor to see the steps. Run from the editor or command line.

```yml
boundary:circle.txt
boundary_refine:true
bounding_box:0,0,0,0
developer_output:false
output_file:circle
resolution:0.5
version:1.1
```

Running the Matlab sript will generate this figure:

![circle_boundary](fig/circle.png)

[Index](README.md)
