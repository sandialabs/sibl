# Reference
# https://scikit-image.org/docs/dev/auto_examples/numpy_operations/plot_structuring_elements.html#sphx-glr-auto-examples-numpy-operations-plot-structuring-elements-py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ptg.pixel_shape import PixelCube as pixel_cube
from ptg.pixel_shape import PixelCylinder as pixel_cylinder
from ptg.pixel_shape import PixelSphere as pixel_sphere

struc_3d = {
    "PixelCube1": pixel_cube(dx=1, pixels_per_len=1),
    "PixelCube2": pixel_cube(dx=2, pixels_per_len=1),
    "PixelCube3": pixel_cube(dx=3, pixels_per_len=1),
    "PixelCylinder3": pixel_cylinder(diameter=3, dx=1, pixels_per_len=1),
    "PixelCylinder5": pixel_cylinder(diameter=5, dx=1, pixels_per_len=1),
    "PixelCylinder7": pixel_cylinder(diameter=7, dx=1, pixels_per_len=1),
    "PixelSphere3": pixel_sphere(diameter=3, pixels_per_len=1),
    "PixelSphere5": pixel_sphere(diameter=5, pixels_per_len=1),
    "PixelSphere7": pixel_sphere(diameter=7, pixels_per_len=1),
}

fig = plt.figure(figsize=(8, 8))

idx = 1

for title, struc in struc_3d.items():
    ax = fig.add_subplot(3, 3, idx, projection=Axes3D.name)
    ax.voxels(struc.mask, edgecolor="black")
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    idx += 1

fig.tight_layout()
plt.show()
