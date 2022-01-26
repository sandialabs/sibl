# Lesson 04: Use with an Input File

To create meshes that can be built through parameterization, the use of an input file will be required.

## Goal

Using an input file, demonstrate how to reproduce the result from the [previous lesson](lesson_03.md).

## Steps

Verify the following files exist:

* [circle_radius_2.txt](../../data/boundary/circle_radius_2.txt) - the boundary `x y` discrete point definition
* [lesson_04.yml](../../data/mesh/lesson_04.yml) - the YAML input file specification

From the command line:

```bash
> conda activate siblenv
> cd ~/sibl
> python geo/src/ptg/main.py -i geo/data/mesh/lesson_04.yml
```

*More to come.*

[Index](README.md)

Previous: [Lesson 03](lesson_03.md)