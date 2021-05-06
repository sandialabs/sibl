import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ptg.pixel_shape import PixelSphere as ps

# shape marching cadence
diam = 3  # pixels, diameter
ppl = 1  # pixels per length
stride = 3  # pixels, distance between sequential anchors
n_shapes = 2  # int, number of sequential shapes added to world
world_bounds = (n_shapes - 1) * stride + diam * ppl
nsd = 3  # number of space dimensions

# world
(n_layers_x, n_cols_y, n_rows_z) = tuple(map(lambda x: world_bounds, range(nsd)))
world = np.zeros([n_layers_x, n_cols_y, n_rows_z], dtype=np.uint8)

inx, iny, inz = np.indices([n_layers_x, n_cols_y, n_rows_z])

# fountain pen metaphor, ink in the shapes to the world
for i in range(n_shapes):
    anchor_x_i = i * stride
    item = ps(anchor_x=anchor_x_i, diameter=diam, pixels_per_len=ppl, verbose=True)

    mask = item.mask
    ox, oy, oz = item.anchor.x, item.anchor.y, item.anchor.z  # offsets

    (npix_x, npix_y, npix_z) = item.mask.shape

    for xx in range(npix_x):
        for yy in range(npix_y):
            for zz in range(npix_z):
                world[xx + ox, yy + oy, zz + oz] = (
                    world[xx + ox, yy + oy, zz + oz] + mask[xx, yy, zz]
                )

# # shapes creation
# ps0 = ps(diameter=diam, pixels_per_len=ppl, verbose=True)
# ps1 = ps(anchor_x=stride, diameter=diam, pixels_per_len=ppl, verbose=True)
#
# shapes = (ps0, ps1)
#
# # world + shapes
# for item in shapes:
#
#     anchor = item.anchor
#     mask = item.mask
#     ox, oy, oz = anchor.x, anchor.y, anchor.z  # offsets
#
#     (npix_x, npix_y, npix_z) = item.mask.shape
#
#     for xx in range(npix_x):
#         for yy in range(npix_y):
#             for zz in range(npix_z):
#                 world[xx + ox, yy + oy, zz + oz] = (
#                     world[xx + ox, yy + oy, zz + oz] + mask[xx, yy, zz]
#                 )

# visualization of world + shapes
# camera_elevation, camera_azimuth = -160, 160  # degrees

fig = plt.figure(figsize=(8, 8))

# view_center = (h, r, r)
# view_radius = r + 1
view_radius = int(np.max(world.shape) // 2 + 1)
view_center = (view_radius, view_radius, view_radius)

ix, iy, iz = 0, 1, 2
xlim = (view_center[ix] + view_radius, view_center[ix] - view_radius)
ylim = (view_center[iy] + view_radius, view_center[iy] - view_radius)
zlim = (view_center[iz] + view_radius, view_center[iz] - view_radius)

index = 1
ax = fig.add_subplot(1, 1, index, projection=Axes3D.name)
# ax.view_init(elev=camera_elevation, azim=camera_azimuth)
ax.voxels(world, linewidth=0.25, edgecolor="black", alpha=0.9)

ax.set_title("pixel_letter_I")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_zlim(zlim)

fig.tight_layout()
plt.show()
