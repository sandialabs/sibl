# Lessons

Learn how to use the *SIBL Mesh Engine* with the lessons below:

* Configuration
  * [00](lesson_00.md). Verify the [configuration](../../../config/README.md).
* Introduction
  * [01](lesson_01.md). Plot a 2D boundary, the first step in meshing a 2D domain.  This will be done interactively with a Python terminal.
  * [02](lesson_02.md). Next, plot the same 2D boundary using a Python script.
  * [03](lesson_03.md). Use the 2D boundary as an input to the mesher, to create a single domain composed of 2D quadrilateral finite elements.
  * [04](lesson_04.md). Use of a `.yml` input file to create the mesh in Lesson 03.
* Unit tests
  * [10](lesson_10.md). Donut - to Chad (Python)
  * [11](lesson_11.md). Quarter Plate - to Ryan (Python)
  * [12](lesson_12.md). Swiss cheese - *to come* - to Adam (MATLAB)
    * concepts
      * the boundaries must be NaN separated for the curve reader to know the curves are separated, and 
      * counter-clockwise is inside the boundary
      * clockwise is not included in the boundary
* Literature Examples
  * [21](lesson_21.md). Flower - *pending* to Adam
  * [22](lesson_22.md). Lake Superior
  * [23](lesson_23.md). Australia
* Applications
  * [40](lesson_40.md). Binary blobs - *to come* - to Chad
  * [41](lesson_41.md). Shepp-Logan phantom - *to come* - to Chad
  * [42](lesson_42.md). Miller phantom - *to come* - to Adam
  * [43](lesson_43.md). MATLAB 3D MRI data set - *to come* - to Chad
* Appendix
  * [a00](lesson_a00.md). Run the engine directly from C++ and the command line, without Python.  (CBH to delete this item and move existing Less a02 to its place.)
  * [a01](lesson_a01.md). Bind C++ for use with Python.
  * [a02](lesson_a02.md). Use MATLAB and text file interop to run the C++ engine and post-process results.
