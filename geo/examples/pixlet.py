import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.mplot3d import Axes3D
from skimage.morphology import skeletonize_3d
from pathlib import Path
from typing import NamedTuple, Tuple

from ptg.pixel_shape import PixelSphere as ps

# utilities
serialize = False
latex = False
if latex:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)


# alphabet
class Letter(NamedTuple):
    """Create the letter index (x=0, y, z) position, in units of inkdrop, as a
    namedtuple, with the following attributes:
    """

    name: str
    path_x: Tuple[int, ...]
    path_y: Tuple[int, ...]
    path_z: Tuple[int, ...]


letter_I = Letter(
    name="I",
    path_x=(0, 1, 2, 3, 4, 5, 6),
    path_y=(4, 4, 4, 4, 4, 4, 4),
    path_z=(4, 4, 4, 4, 4, 4, 4),
)

letter_J = Letter(
    name="J",
    path_x=(4, 3, 2, 1, 2, 3, 4, 5, 6),
    path_y=(6, 6, 5, 4, 3, 2, 2, 2, 2),
    path_z=(4, 4, 4, 4, 4, 4, 4, 4, 4),
)

letter = letter_J
assert len(letter.path_x) == len(letter.path_y) == len(letter.path_z)

# letters make with 5x5 grid of possible inkdrops
# droplet_grid_len = 5

# shape marching cadence
diam = 3  # pixels, diameter
ppl = 1  # pixels per length
stride = 1  # pixels, distance between sequential anchors
# n_shapes = 5  # int, number of sequential shapes added to world
n_shapes = len(letter.path_x)  # int, number of sequential shapes added to world
# world_bounds = (n_shapes - 1) * stride + diam * ppl
world_bounds = (
    max(map(lambda i: max(i), (letter.path_x, letter.path_y, letter.path_z))) + diam
)  # pixels
nsd = 3  # number of space dimensions

# world
(n_layers_x, n_cols_y, n_rows_z) = tuple(map(lambda x: world_bounds, range(nsd)))
world = np.zeros([n_layers_x, n_cols_y, n_rows_z], dtype=np.uint8)

inx, iny, inz = np.indices([n_layers_x, n_cols_y, n_rows_z])

# fountain pen metaphor, ink in the shapes to the world
# for i in range(n_shapes):
for i, (xi, yi, zi) in enumerate(zip(letter.path_x, letter.path_y, letter.path_z)):
    # anchor_x_i = i * stride
    # item = ps(anchor_x=anchor_x_i, diameter=diam, pixels_per_len=ppl, verbose=True)
    item = ps(
        anchor_x=xi,
        anchor_y=yi,
        anchor_z=zi,
        diameter=diam,
        pixels_per_len=ppl,
        verbose=True,
    )

    mask = item.mask
    ox, oy, oz = item.anchor.x, item.anchor.y, item.anchor.z  # offsets

    (npix_x, npix_y, npix_z) = item.mask.shape

    for xx in range(npix_x):
        for yy in range(npix_y):
            for zz in range(npix_z):
                world[xx + ox, yy + oy, zz + oz] = (
                    world[xx + ox, yy + oy, zz + oz] + mask[xx, yy, zz]
                )

# visualization of world + shapes
# camera_elevation, camera_azimuth = -160, 160  # degrees

n_fig_rows, n_fig_cols = 1, 2
# fig = plt.figure(figsize=(8, 8))
fig = plt.figure()

# view_center = (h, r, r)
# view_radius = r + 1
view_radius = int(np.max(world.shape) // 2 + 1)
view_center = (view_radius, view_radius, view_radius)

ix, iy, iz = 0, 1, 2
xlim = (view_center[ix] + view_radius, view_center[ix] - view_radius)
ylim = (view_center[iy] + view_radius, view_center[iy] - view_radius)
zlim = (view_center[iz] + view_radius, view_center[iz] - view_radius)

index = 1
ax = fig.add_subplot(n_fig_rows, n_fig_cols, index, projection=Axes3D.name)
# ax.view_init(elev=camera_elevation, azim=camera_azimuth)
ax.voxels(world, linewidth=0.25, edgecolor="black", alpha=0.9)

ax.set_title("(a)")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r"$z$")
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_zlim(zlim)

# fig.tight_layout()
# plt.show()


# skeletonize
# https://scikit-image.org/docs/dev/auto_examples/edges/plot_skeleton.html
# Use the Lee 1994 algorithm for 3D shapes
# References
# [Lee94] T.-C. Lee, R.L. Kashyap and C.-N. Chu, Building skeleton models
#   via 3-D medial surface/axis thinning algorithms.
#   Computer Vision, Graphics, and Image Processing, 56(6):462-478, 1994.
# [Zha84] A fast parallel algorithm for thinning digital patterns,
#   T. Y. Zhang and C. Y. Suen, Communications of the ACM,
#   March 1984, Volume 27, Number 3.
skeleton = skeletonize_3d(world)

# fig = plt.figure(figsize=(8, 8))

index += 1
ax = fig.add_subplot(n_fig_rows, n_fig_cols, index, projection=Axes3D.name)
# ax.view_init(elev=camera_elevation, azim=camera_azimuth)
# ax.voxels(world, linewidth=0.25, edgecolor="black", alpha=0.9)
ax.voxels(skeleton, linewidth=0.25, edgecolor="black", alpha=0.9)

ax.set_title("(b)")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r"$z$")
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_zlim(zlim)

fig.tight_layout()
plt.show()
# plt.show(block=False)

if serialize:
    extension = ".pdf"
    filename = (
        Path(__file__).stem
        + "_"
        + letter.name
        + "_drop_"
        + str(n_shapes)
        + "_diam_"
        + str(diam)
        + "_stri_"
        + str(stride)
        + extension
    )
    fig.savefig(filename, bbox_inches="tight", pad_inches=0)
    print(f"Serialized to {filename}")


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
