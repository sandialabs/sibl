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
    "PixelCylinder3": pixel_cylinder(diameter_outer=3, height=1, pixels_per_len=1),
    "PixelCylinder5": pixel_cylinder(diameter_outer=5, height=1, pixels_per_len=1),
    "PixelCylinder7": pixel_cylinder(diameter_outer=7, height=1, pixels_per_len=1),
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


"""
Copyright 2023 Sandia National Laboratories

Notice: This computer software was prepared by National Technology and Engineering Solutions of
Sandia, LLC, hereinafter the Contractor, under Contract DE-NA0003525 with the Department of Energy
(DOE). All rights in the computer software are reserved by DOE on behalf of the United States
Government and the Contractor as provided in the Contract. You are authorized to use this computer
software for Governmental purposes but it is not to be released or distributed to the public.
NEITHER THE U.S. GOVERNMENT NOR THE CONTRACTOR MAKES ANY WARRANTY, EXPRESS OR IMPLIED, OR ASSUMES
ANY LIABILITY FOR THE USE OF THIS SOFTWARE. This notice including this sentence must appear on any
copies of this computer software. Export of this data may require a license from the United States
Government.
"""
