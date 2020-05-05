# Three-Point Angular Velocity (TPAV)

## Abstract

Given velocity of three points on a quasi-rigid body, calculate the body's angular velocity.

## Methods

The theoretical development is forthcoming, to appear in a SAND report (as of 2020-05-05).

### Input

The three-point angular velocity algorithm is applied to a mildly deformable (quasi-rigid) body, and compared to a rigid body dynamics simulation reference.  

* The rigid body reference data is contained in `input/rigid_reference.csv`.  
* The deformable body output data from SSM is contained in `input/history.csv`. 
* The `.json` file used by XYFigure to post-process the two input files is `tpav_postpro.json`.

### Output
