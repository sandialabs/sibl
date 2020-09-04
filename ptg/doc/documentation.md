# Documentation

## Required Keys

```bash
bezier-type: ["curve", "surface", "solid"]
control-nets:
control-points:
data-path:
```

# Optional Keys

```bash

bezier-lines-color: "black"
bezier-lines-shown: False
bezier-linewidth: 1.0

bezier-points-color: "blue"
bezier-points-shown: True
bezier-points-size: 10

camera-azimuth: None
camera-elevation: None

control-nets-shown: [0] # show at least the first net
control-nets-linestyle: "dashed"
control-nets-linewidth: 0.8

control-points-color: "red"
control-points-label: False  # better key needed
control-points-label-color: "black"
control-points-path: False
control-points-marker: "^"
control-points-shown: True
control-points-size: 50

nti_division: 1 (positive integer)

surface-triangulation: True # only for bezier-type = surface
triangulation-alpha: 1.0 # only for bezier-type = surface

xlabel: "x"
xlim: None
ylabel: "y"
ylim: None
zlabel: "z"
zlim: None

```