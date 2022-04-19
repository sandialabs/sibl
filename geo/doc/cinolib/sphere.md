
# sphere

## Objective

* Compare mesh created with Sculpt to Gen-Adapt-Ref-for-Hexmeshing.

## Materials

* sphere.obj file on [data page](../../data/obj/README.md)
* [Gena](../../doc/cinolib/gena.md)
* Sculpt (to come)

## Workflow

See [Stanford bunny workflow](https://github.com/sandialabs/sibl/blob/master/geo/doc/cinolib/bunny.md#workflow)

## Methods

One the `[cbh@atlas]` machine:

```bash
cd ~/Gen-Adapt-Ref-for-Hexmeshing/build
./make_grid --surface --input_mesh_path=/Users/cbh/sibl/geo/data/obj/sphere.obj --output_grid_path=/Users/cbh/sibl/geo/data/mesh/sphere.mesh --use_octree --project_mesh=true
```

In a web browser, open https://www.hexalab.net/, then open the following files:

* `sphere.mesh`
* `sphere_conforming.mesh`
* `sphere_projected.mesh`

The view settings,
[`HLsettings-default.txt`](fig/HLsettings-default.txt),
are used with hexalab.

| Default View | Alternative View |
|:--:|:--:|
| sphere.obj</br> ![../fig/sphere.png] | |
| sphere.mesh</br> ![](fig/sphere-default.png) | ![](fig/sphere-alt.png) |
| sphere_conforming.mesh</br> ![](fig/sphere-conforming-default.png) | ![](fig/sphere-conforming-alt.png) |
| sphere_projected.mesh ![](fig/sphere-projected-default.png) | ![](fig/sphere-projected-alt.png) |

