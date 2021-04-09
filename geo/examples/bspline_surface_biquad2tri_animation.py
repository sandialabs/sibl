"""
Example:
> cd ~/sibl/geo/examples
> conda activate siblenv
> python bspline_surface_biquad2tri_animation.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.tri as mtri
from pathlib import Path

import ptg.bspline as bsp
import ptg.view_bspline as vbsp

# Utilites
ix, iy, iz = 0, 1, 2  # xyz indicies, avoid magic numbers
control_net_shown = True  # True lets control net be drawn, False skips it
control_points_shown = True
serialize = False
latex = False
if latex:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)

# The first and only figure
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_proj_type("ortho")
ax.view_init(elev=0, azim=0)
# ax.set_proj_type("persp")

# plot3d api
# https://matplotlib.org/stable/api/_as_gen/mpl_toolkits.mplot3d.axes3d.Axes3D.html?highlight=set_box_aspect#mpl_toolkits.mplot3d.axes3d.Axes3D.set_box_aspect

# ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r"$z$")

xmax = 1
# ax.set_xlim([-xmax, 0.0])
ax.set_xlim([-xmax, 0])
ax.set_ylim([0, 1])
ax.set_zlim([0, 1])

# ax.set_box_aspect([2.5, 1, 1])
ax.set_box_aspect([1, 1, 1])

interval = np.arange(0, xmax + 1, 1)

# ax.set_xticks(interval)
ax.set_xticks([])  # show no ticks
# ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_zticks([0, 1])
# ax.set_axis_off()  # turns off all three axes
ax.grid(False)
# ax.tick_params(axis="x", color="red")
ax.xaxis.label.set_color("red")
# ax.xaxis.set_color("red")
ax.tick_params(axis="x", colors="blue")
# ax.spines["bottom"].set_color("red")
# ax.w_zaxis  # <- the z axis
ax.w_xaxis.line.set_color("white")
# ax.set_axis_off()
# ax.xaxis.set_alpha(0.5)
# ax.xaxis.spline.set_color("magenta")
# ax.xaxis.set_visible(False)
# Get rid of the panes
# ax.w_xaxis.line.set_color((1.0, 0.0, 0.0, 0.0))
# ax.w_yaxis.set_pane_color((0.0, 1.0, 0.0, 0.0))

# Common to all Bspline surfaces used herein
kv = (0.0, 0.0, 0.0, 1.0, 1.0, 1.0)  # knot vector for t, u parameters
quadratic = 2  # quadratic
nbi = 2  # number of bisections per knot interval

# Compose collection of Bspline surfaces as a group of control_points that describe
# each surface.
xneg0 = (
    ((0.0, 0.0, 0.0), (0.0, 0.0, 0.5), (0.0, 0.0, 1.0)),
    ((0.0, 0.5, 0.0), (0.0, 0.5, 0.5), (0.0, 0.5, 1.0)),
    ((0.0, 1.0, 0.0), (0.0, 1.0, 0.5), (0.0, 1.0, 1.0)),
)

# xneg1 = (
#     ((1.0, 0.0, 0.0), (1.0, 0.0, 0.5), (1.0, 0.0, 1.0)),
#     ((1.0, 0.25, 0.0), (1.0, 0.75 / 2.0, 0.5), (1.0, 0.5, 1.0)),
#     ((1.0, 0.50, 0.0), (1.0, 1.50 / 2.0, 0.5), (1.0, 1.0, 1.0)),
# )
#
# xneg2 = (
#     ((2.0, 0.0, 0.0), (2.0, 0.0, 0.5), (2.0, 0.0, 1.0)),
#     ((2.0, 0.0, 0.0), (2.0, 0.25, 0.5), (2.0, 0.5, 1.0)),
#     ((2.0, 0.0, 0.0), (2.0, 0.5, 0.5), (2.0, 1.0, 1.0)),
# )
#
# xneg3 = (
#     ((3.0, 0.0, 0.0), (3.0, 0.0, 0.5), (3.0, 0.0, 1.0)),
#     ((3.0, 0.0, 0.0), (3.0, 0.5, 0.5), (3.0, 1.0, 1.0)),
#     ((3.0, 0.0, 0.0), (3.0, 0.5, 0.0), (3.0, 1.0, 0.0)),
# )

# surfaces = (xneg0,)
# surfaces = (xneg0, xneg1, xneg2, xneg3)
scaffolds = (xneg0,)
kvs = (kv,)  # knot vectors

patches = tuple(
    bsp.SurfaceClientData(
        knot_vector_t=kv,
        knot_vector_u=kv,
        coefficients=scaffold,
        degree_t=quadratic,
        degree_u=quadratic,
        n_bisections=nbi,
        color=vbsp.colors[i],
    )
    for i, (scaffold, kv) in enumerate(zip(scaffolds, kvs))
)


if control_net_shown:
    pass

if control_points_shown:
    for p in patches:
        cp_x = np.array(p.coefficients)[:, :, ix].flatten()
        cp_y = np.array(p.coefficients)[:, :, iy].flatten()
        cp_z = np.array(p.coefficients)[:, :, iz].flatten()

        ax.plot3D(cp_x, cp_y, cp_z, **vbsp.defaults["control_points_kwargs"])

for p in patches:

    S = bsp.Surface(
        knot_vector_t=p.knot_vector_t,
        knot_vector_u=p.knot_vector_u,
        coefficients=p.coefficients,
        degree_t=p.degree_t,
        degree_u=p.degree_u,
        n_bisections=p.n_bisections,
    )
    (surf_x, surf_y, surf_z) = S.evaluations

    ax.plot3D(
        surf_x.flatten(),
        surf_y.flatten(),
        surf_z.flatten(),
        **vbsp.defaults["evaluation_points_kwargs"],
    )

    u, t = np.meshgrid(S.evaluation_times_u, S.evaluation_times_t)
    u, t = u.flatten(), t.flatten()
    tri = mtri.Triangulation(u, t)

    triangulation_kwargs = dict(triangles=tri.triangles)
    triangulation_kwargs.update(**vbsp.defaults["surface_kwargs"])

    current_color_kwargs = dict(color=p.color)
    triangulation_kwargs.update(current_color_kwargs)

    ax.plot_trisurf(
        surf_x.flatten(), surf_y.flatten(), surf_z.flatten(), **triangulation_kwargs
    )

# Back to the singleton figure
plt.show()

if serialize:
    extension = ".pdf"
    filename = Path(__file__).name + extension
    fig.savefig(filename, bbox_inches="tight", pad_inches=0)
    print(f"Serialized to {filename}")
