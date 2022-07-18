# cube minus sphere

## Objective

* Compare mesh created with Gen-Adapt-Ref-for-Hexmeshing (GENA) to Sculpt.

## Materials

* `cube_minus_sphere.obj` file on the [data page](../../data/obj/README.md)
* [Gena](../../doc/cinolib/gena.md)
* [HexaLab](https://www.hexalab.net)
* Sculpt (to come)

## Workflow

See [Stanford bunny workflow](https://github.com/sandialabs/sibl/blob/master/geo/doc/cinolib/bunny.md#workflow)

## Methods

On the `[cbh@atlas]` machine:

```bash
cd ~/Gen-Adapt-Ref-for-Hexmeshing/build
./make_grid --surface --input_mesh_path=/Users/cbh/sibl/geo/data/obj/cube_minus_sphere.obj --output_grid_path=/Users/cbh/sibl/geo/data/mesh/cube_minus_sphere.mesh --use_octree --project_mesh=true
```

With https://www.hexalab.net/, open the following files:

* `cube_minus_sphere.mesh`
* `cube_minus_sphere_conforming.mesh`
* `cube_minus_sphere_projected.mesh`

The view settings,
[`HLsettings-default.txt`](fig/HLsettings-default.txt),
are used with hexalab.

| Default View | Alternative View |
|:--:|:--:|
| cube_minus_sphere.obj</br> <img src="../../data/obj/cube_minus_sphere_default.png" height="200"> | <img src="../../data/obj/cube_minus_sphere_alt.png" height="200"> |
| cube_minus_sphere.mesh</br> <img src="fig/cube-minus-sphere-default.png" width="300"> | <img src="fig/cube-minus-sphere-alt.png" width="400"> |
| cube_minus_sphere_conforming.mesh</br> <img src="fig/cube-minus-sphere-conforming-default.png" width="300"> | <img src="fig/cube-minus-sphere-conforming-alt.png" width="400"> |
| cube_minus_sphere_projected.mesh <img src="fig/cube-minus-sphere-projected-default.png" width="300"> | <img src="fig/cube-minus-sphere-projected-alt.png" width="400"> |
