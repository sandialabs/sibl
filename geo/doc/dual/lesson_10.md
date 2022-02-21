# Lesson 10: Donut

## Goals

Demonstrate mesh creation for a domain with a circular outer and inner boundaries.

## Steps

### Create the boundaries

The [`donut.py`](lesson_10/donut.py) file is used to create the `x y` boundary
pair file [`donut.txt`](lesson_10/donut.txt).

* The the outer boundary:
  * is shown in orange discrete points connected with a light blue line, and
  * proceeds in a counter-clockwise manner.
* The inner boundary:
  * is shown in red discrete points connected with a light green line, and 
  * proceeds in a clockwise manner.

The left image shows a full view of the boundaries.
The right image shows a zoomed in view of the beginning and end of each boundary.

| Full view | Zoomed view |
|:--:|:--:|
| ![donut](fig/donut.png) | ![donut_zoomed](fig/donut_zoomed.png) |

### Create the `.yml` input file

The [`lesson_10.yml`](lesson_10/lesson_10.yml) is used to run the *SIBL Mesh Engine* as follows:

```bash
> conda activate siblenv
> cd ~/sibl/geo/doc/dual/lesson_10
> pydual -i lesson_10.yml
SIBL Mesh Engine initialized.
driver: /Users/chovey/sibl/geo/src/ptg/main.py
Dualization initiated.
input: lesson_10.yml
The database is {'version': 1.4, 'io_path': '~/sibl/geo/doc/dual/lesson_10/', 'boundary': 'donut.txt', 'bounding_box': [[-8.0, -8.0], [8.0, 8.0]], 'resolution': 1.0, 'output_file': 'lesson_10_mesh', 'boundary_refine': True, 'developer_output': False, 'figure': {'boundary_shown': True, 'dpi': 200, 'elements_shown': True, 'filename': 'lesson_10_figure', 'format': 'pdf', 'frame': True, 'grid': False, 'label_x': '$x$', 'label_y': '$y$', 'latex': False, 'save': True, 'show': False, 'size': [6.0, 6.0], 'title': 'Lesson 10'}}
This input file has version 1.4
io_path: /Users/chovey/sibl/geo/doc/dual/lesson_10
Current working directory changed to /Users/chovey/sibl/geo/doc/dual/lesson_10
yml specified boundary file: donut.txt
  located boundary file at:
  donut.txt
deciding this loop is : in
deciding this loop is : out
inCurve with 72 points
outCurve with 72 points
Determining derivative...
Determining derivative...
Setting tangent and angle...
Setting tangent and angle...
Finding corners...
Finding corners...
Finding features...
Done with features.
Finding features...
Done with features.
QuadMesh constructor complete
Computing Mesh
Size of my nodes: 0
Size of my Primal nodes: 869
Size of my Primal Polys: 816
Unique loop size: 765
  Saved figure to lesson_10_figure.pdf
SIBL Mesh Engine completed.
Dualization is complete.
SIBL Mesh Engine completed.
```

### Outputs

The following will appear in the specified `io_path` folder:

* Mesh file [`lesson_10_mesh.inp`](lesson_10/lesson_10_mesh.inp)
* Image file [`lesson_10_figure.pdf`](lesson_10/lesson_10_figure.pdf)

## Developer Output

### Quad Tree

![quadtree](fig/NestedCircle4date2021-12-08.png)

### Primal

![](fig/NestedCircle2date2021-12-08.png)

### Primal + Dual

![](fig/NestedCircleDPdate2021-12-08.png)

### Dual + Trim + Project

![](fig/NestedCircle3date2021-12-08.png)

### Dual + Trim + Project + Snap

![](fig/NestedCircle6date2021-12-08.png)

### Dual + Trim + Project + Snap + Smooth

![](fig/NestedCircle5date2021-12-08.png)

[Index](README.md)
