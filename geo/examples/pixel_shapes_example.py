# Reference
# https://scikit-image.org/docs/dev/auto_examples/numpy_operations/plot_structuring_elements.html#sphx-glr-auto-examples-numpy-operations-plot-structuring-elements-py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ptg.pixel_shape import PixelCube as pixel_cube
from ptg.pixel_shape import PixelCylinder as pixel_cylinder
from ptg.pixel_shape import PixelSphere as pixel_sphere

struc_3d = {
    "PixelCube1": pixel_cube(width=1, pixels_per_len=2),
    "PixelCube2": pixel_cube(width=2, pixels_per_len=2),
    "PixelCube3": pixel_cube(width=3, pixels_per_len=2),
    "PixelCylinder1": pixel_cylinder(radius=1, height=1, pixels_per_len=2),
    "PixelCylinder2": pixel_cylinder(radius=2, height=1, pixels_per_len=2),
    "PixelCylinder3": pixel_cylinder(radius=3, height=1, pixels_per_len=2),
    "PixelSphere1": pixel_sphere(radius=1, pixels_per_len=2),
    "PixelSphere2": pixel_sphere(radius=2, pixels_per_len=2),
    "PixelSphere3": pixel_sphere(radius=3, pixels_per_len=2),
}

fig = plt.figure(figsize=(8, 8))

idx = 1

for title, struc in struc_3d.items():
    ax = fig.add_subplot(3, 3, idx, projection=Axes3D.name)
    ax.voxels(struc.mask)
    ax.set_title(title)
    ax.set_xlabel("z")
    ax.set_ylabel("y")
    ax.set_zlabel("x")
    idx += 1

fig.tight_layout()
plt.show()
