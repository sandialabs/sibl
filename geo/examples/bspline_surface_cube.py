"""This module recovers a six-sided (bottom, top, lateral) surfaces of a cube.

Example:
> cd ~/sibl/geo/examples
> conda activate siblenv
> python bspline_surface_cube.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

import ptg.bspline as bsp

# Utilites
ix, iy, iz = 0, 1, 2  # xyz indicies, avoid magic numbers

# The first and only figure
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

# Common to all Bspline surfaces used herein
kv_t = (0.0, 0.0, 1.0, 1.0)  # knot vector for t parameter
kv_u = (0.0, 0.0, 1.0, 1.0)  # knot vector for u parameter
degree_t = 1  # linear
degree_u = 1  # linear
nbi = 2  # number of bisections per knot interval

# Compose collection of Bspline surfaces as a group of control_points that describe
# each surface.
surfaces = (
    (((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)), ((0.0, 1.0, 0.0), (0.0, 1.0, 1.0)),),
    (((1.0, 0.0, 0.0), (1.0, 0.0, 1.0)), ((1.0, 1.0, 0.0), (1.0, 1.0, 1.0)),),
)

colors = ("tab:blue", "tab:orange")

for control_points, surface_color in zip(surfaces, colors):
    S = bsp.Surface(
        kv_t, kv_u, control_points, degree_t, degree_u, n_bisections=nbi, verbose=True,
    )
    (surf_x, surf_y, surf_z) = S.evaluations

    S_evaluations_view_config = dict(
        alpha=0.9,
        color="navy",
        linestyle="dashed",
        linewidth=0,
        marker=".",
        markersize=4,
    )

    ax.plot3D(
        surf_x.flatten(),
        surf_y.flatten(),
        surf_z.flatten(),
        **S_evaluations_view_config
    )

    u, t = np.meshgrid(S.evaluation_times_u, S.evaluation_times_t)
    u, t = u.flatten(), t.flatten()
    tri = mtri.Triangulation(u, t)
    S_triangulation_view_config = dict(
        alpha=0.8, color=surface_color, triangles=tri.triangles
    )
    ax.plot_trisurf(
        surf_x.flatten(),
        surf_y.flatten(),
        surf_z.flatten(),
        **S_triangulation_view_config
    )

# Back to the singleton figure
plt.show()
