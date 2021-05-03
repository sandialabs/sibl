# Encode/Decode Unit Test

## Encoding

We select (for the present time) a singleton member of a 3D physical shape set in (0, 1, 2, 3, 4, 5, 6, 7 , 8, 9), described by an 

* **atlas** 
  * also known as a "prototype", "factory", or "font factory"
  * defined in space by a local coordinate measures (x, y, z),
  * with domain [x0, x1], [y0, y1], [z0, z1], 
    * $\omega$ subset R3
    * known as a "bounding box"
* **scaled** 
  * along the local axes (e1, e2, e3) by scaling constants (sx, sy, sz)
    * subset R3+ and 
    * such that the Jacobian of the transformation is positive, J > 0, then
* **rotated**, in succession, by
  * yaw (rz, inferior-to-superior local axis), in [-pi, pi]
  * pitch (ry, right-to-left local axis), in [-pi, pi], and 
  * roll (rx, posterior-to-anterior local axis), in [-pi, pi], then
* **translated** 
  * into the parent domain through translation (tx, ty, tz) subset R3, 
  * to be fully contain in the parent domain (defined below)

## Decoding

We define the **decode** process as inputing a 3D rectangular domain

* of extends [X0, X1], [Y0, Y1], [Z0, Z1], known as the "parent domain" $\Omega$ subset R3
* stored in a concatenated series of 2D elevations
  * parameterized by h along the Z-axis,
  * subset of R2, 
* composed of a population of regular-shaped pixels, 
  * each with a location (px, py, pz) member of P0, and 
  * intensity (pi) subset J in [0, 1], 
  
to both *predict* and *reconstruct* a 3D shape known, *a priori*, 

* to be a member of a 3D physical shape set, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
* to have *intrinsic* transformations from its atlas of (sx, sy, sz), 
* to have *extrinsic* transformations (rx, ry, rz), and
* to have *exogenous* transformations (ux, uy, uz).

### Data Standards

DICOM, Digital Imaging and Communications in Medicine, is a medical imaging
standard, but can be overly burdensome if only volume information is desired
since the DICOM header is memory intensive.

NIfTI, Neuroimaging Informatics Technology Initiative (NIfTI) is a DICOM
alternative that stores only volume-specific header information (e.g., 
position, rotation, resolution) within the volumetric data.

### Deep Learning

* Deep Learning as a possible decode solution.

Input: 

* Black and white 1d slices

Ouput: 

* [class, sx, sy, sz, rx, ry, rz, ux, uy, uz]
* class, three scaling constants, three rotations, three translations

Training data: 

* x: Black white 1d slices of class 0
* y: ["class 0", 1, 1, 1, 0, 0, 0, 0, 0, 0]

### Signal Processing

* Signal processing, in particular, cross-correlation, as a possible decode solution.

References:

* [3D MNIST](https://www.kaggle.com/daavoo/3d-mnist)
* [Spatial Transformer Network Tutorial](https://pytorch.org/tutorials/intermediate/spatial_transformer_tutorial.html)

