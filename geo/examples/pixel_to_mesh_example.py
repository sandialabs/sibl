# https://matplotlib.org/stable/gallery/mplot3d/voxels.html

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ptg.pixel_shape import PixelCylinder as pixel_cylinder

# create a world of pixel dimensions
n_layers_z, n_rows_y, n_cols_x = 1, 4, 6
# indices
inz, iny, inx = np.indices([n_layers_z, n_rows_y, n_cols_x])
# world of extents dimensions and zero voxels throughout
world = np.zeros([n_layers_z, n_rows_y, n_cols_x], dtype=np.uint8)

# offsetz, offsety, offsetx = 0.0, 0.0, 0.0
offsetz, offsety, offsetx = 0.0, 1.0, 2.0

r = 1  # radius
h = 1  # height
pc = pixel_cylinder(
    radius=r,
    height=h,
    pixels_per_len=1,
    anchor_x=offsetx,
    anchor_y=offsety,
    anchor_z=offsetz,
)
anchor = pc.anchor
mask = pc.mask
oz, oy, ox = anchor.z, anchor.y, anchor.x  # offsets

(npix_z, npix_y, npix_x) = pc.mask.shape

for zz in range(npix_z):
    for yy in range(npix_y):
        for xx in range(npix_x):
            world[zz + oz, yy + oy, xx + ox] = (
                world[zz + oz, yy + oy, xx + ox] + mask[zz, yy, xx]
            )

camera_elevation, camera_azimuth = 15, -35  # degrees

fig = plt.figure(figsize=(8, 8))

# view_center = (h, r, r)
# view_radius = r + 1
view_radius = int(np.max(world.shape) / 2.0)
view_center = (view_radius, view_radius, view_radius)

ix, iy, iz = 2, 1, 2
xlim = (view_center[ix] + view_radius, view_center[ix] - view_radius)
ylim = (view_center[iy] + view_radius, view_center[iy] - view_radius)
zlim = (view_center[iz] + view_radius, view_center[iz] - view_radius)

index = 1
ax = fig.add_subplot(1, 1, index, projection=Axes3D.name)
ax.view_init(elev=camera_elevation, azim=camera_azimuth)
# ax.voxels(pc.mask, edgecolor="black")
ax.voxels(world, edgecolor="black")
# plot anchor point
# anchor = pc.anchor
ax.plot3D(anchor.z, anchor.y, anchor.x, color="red", marker="o")
# plot bounding box

ax.set_title("cylinder")
ax.set_xlabel("z")
ax.set_ylabel("y")
ax.set_zlabel("x")
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_zlim(zlim)

fig.tight_layout()
plt.show()
