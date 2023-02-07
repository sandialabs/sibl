# https://matplotlib.org/stable/gallery/mplot3d/voxels.html

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from ptg.pixel_shape import PixelCylinder as pixel_cylinder
from ptg.pixel_shape import PixelQuarterCylinder as pixel_quarter_cylinder
from ptg.pixel_shape import BoundingBoxLines as bbl


offsetx, offsety, offsetz = 0.0, 0.0, 0.0
# offsetx, offsety, offsetz = 0.0, 1.0, 2.0

draw_cylinder = True
draw_cylinder = False

if draw_cylinder:
    max_len = 12
else:
    max_len = 6

ppl = 3  # pixels per length

if draw_cylinder:
    # cylinder primitive
    pixel_shape = pixel_cylinder(
        diameter_inner=6,
        diameter_outer=max_len,
        height=1,
        pixels_per_len=ppl,
        anchor_x=offsetx,
        anchor_y=offsety,
        anchor_z=offsetz,
    )
else:
    # quarter-cylinder primitive
    pixel_shape = pixel_quarter_cylinder(
        height=1,
        radius_inner=3,
        radius_outer=max_len,
        pixels_per_len=ppl,
        anchor_x=offsetx,
        anchor_y=offsety,
        anchor_z=offsetz,
    )


# world start
# create a world of pixel dimensions
# n_layers_x, n_cols_y, n_rows_z = 1, 4, 6
# n_size = 40  # pixels
n_size = max_len * ppl  # pixels
n_layers_x, n_cols_y, n_rows_z = 5, n_size, n_size
# indices
inx, iny, inz = np.indices([n_layers_x, n_cols_y, n_rows_z])
# world of extents dimensions and zero voxels throughout
world = np.zeros([n_layers_x, n_cols_y, n_rows_z], dtype=np.uint8)
# world stop

anchor = pixel_shape.anchor
mask = pixel_shape.mask
ox, oy, oz = anchor.x, anchor.y, anchor.z  # offsets

(npix_x, npix_y, npix_z) = pixel_shape.mask.shape

for xx in range(npix_x):
    for yy in range(npix_y):
        for zz in range(npix_z):
            world[xx + ox, yy + oy, zz + oz] = (
                world[xx + ox, yy + oy, zz + oz] + mask[xx, yy, zz]
            )

# camera_elevation, camera_azimuth = 15, -35  # degrees
# camera_elevation, camera_azimuth = -150, 150  # degrees
# camera_elevation, camera_azimuth = -170, 160  # degrees
camera_elevation, camera_azimuth = -160, 160  # degrees

fig = plt.figure(figsize=(8, 8))

# view_center = (h, r, r)
# view_radius = r + 1
view_radius = int(np.max(world.shape) / 2.0)
view_center = (view_radius, view_radius, view_radius)

ix, iy, iz = 0, 1, 2
xlim = (view_center[ix] + view_radius, view_center[ix] - view_radius)
ylim = (view_center[iy] + view_radius, view_center[iy] - view_radius)
zlim = (view_center[iz] + view_radius, view_center[iz] - view_radius)

index = 1
ax = fig.add_subplot(1, 1, index, projection=Axes3D.name)
ax.view_init(elev=camera_elevation, azim=camera_azimuth)
# ax.voxels(pixel_shape.mask, edgecolor="black")
ax.voxels(world, linewidth=0.25, edgecolor="black", alpha=0.5)
# plot anchor point
# anchor = pixel_shape.anchor
ax.plot3D(anchor.x, anchor.y, anchor.z, color="magenta", markersize=10, marker="o")
# plot bounding box

# draw bounding box rows
_bbl = bbl(pixel_shape)  # bounding box lines

for pts in _bbl.edges_dx:
    ax.plot3D(
        pts[:, ix],
        pts[:, iy],
        pts[:, iz],
        alpha=0.8,
        linestyle="solid",
        color="red",
        linewidth=2,
    )

for pts in _bbl.edges_dy:
    ax.plot3D(
        pts[:, ix],
        pts[:, iy],
        pts[:, iz],
        alpha=0.8,
        linestyle="solid",
        color="green",
        linewidth=2,
    )

for pts in _bbl.edges_dz:
    ax.plot3D(
        pts[:, ix],
        pts[:, iy],
        pts[:, iz],
        alpha=0.8,
        linestyle="solid",
        color="blue",
        linewidth=2,
    )

ax.set_title("cylinder")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_zlim(zlim)

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
