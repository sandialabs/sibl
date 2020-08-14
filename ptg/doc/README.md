# doc

## Deep Learning Part

Input: 

* Black and white 1d slices

Ouput: 

* [class, sx, sy, sz, rx, ry, rz, tx, ty, tz]
* class, three scaling constants, three rotations, three translations

Training data: 

* x: Black white 1d slices of class 0
* y: ["class 0", 1, 1, 1, 0, 0, 0, 0, 0, 0]

References:

* [3D MNIST](https://www.kaggle.com/daavoo/3d-mnist)
