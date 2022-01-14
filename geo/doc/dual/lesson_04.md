# Lesson 04: Use with an Input File

To create meshes that can be built through parameterization, the use of an input file will be required.

## Goal

Using an input file, demonsrate how to reproduce the result from the previous lesson.

Verify the following files exist:

* [circle_radius_2.csv](../../data/boundary/circle_radius_2.csv) - the boundary `(x, y)` discrete point definition
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
