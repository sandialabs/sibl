# Lessons

Learn how to use the *SIBL Mesh Engine* with the lessons below:

* Introduction - Python with C++ library
  * [00](lesson_00.md). Verify the [configuration](../../../config/README.md).
  * [01](lesson_01.md). Plot a 2D boundary, the first step in meshing a 2D domain.  This will be done interactively with a Python terminal.
  * [02](lesson_02.md). Next, plot the same 2D boundary using a Python script.
  * [03](lesson_03.md). Use the 2D boundary as an input to the mesher, to create a single domain composed of 2D quadrilateral finite elements.
  * [04](lesson_04.md). Use of a `.yml` input file to create the mesh in Lesson 03.
    * [04b](lesson_04b.md). Mesh smoothing of the mesh created in Lesson 04.
    * [04c](lesson_04c.md). Mesh smoothing improves the minimum scaled Jacobians of the mesh created in Lesson 04.
  * [05](lesson_05.md). The `.yml` configuration file options
  * [06](lesson_06.md). Developer output and `.dev` files
* Introduction - C++ executable with and without MATLAB
  * [07](lesson_07.md). Compile the C++ source into an executable, use it with and without MATLAB.
  * [08](lesson_08.md). Swiss cheese - use C++ and MATLAB with multiple curves to form a complex boundary.
  * [09](lesson_09.md). Build and Debug `dual.out` on macOS
* Unit tests
  * [10](lesson_10.md). Donut - demonstrate mesh creation for a domain with a circular outer and inner boundaries.
  * [11](lesson_11.md). Quarter Plate
* Literature Examples
  * *To come.* [21](lesson_21.md). Flower
  * *To come.* [22](lesson_22.md). Lake Superior
  * *To come.* [23](lesson_23.md). Australia
* Applications
  * *To come.* [40](lesson_40.md). Binary blobs
  * *To come.* [41](lesson_41.md). Shepp-Logan phantom
  * *To come.* [42](lesson_42.md). Miller phantom
  * *To come.* [43](lesson_43.md). MATLAB 3D MRI data set
* Appendix
  * [a00](lesson_a00.md). Bind C++ for use with Python.
