"""This module recovers a six-sided (bottom, top, lateral) surfaces of a cube.

Example:
> cd ~/sibl/geo/examples
> conda activate siblenv
> python bspline_surface_cube_degen_quadratic.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

import ptg.bspline as bsp
import ptg.view_bspline as vbsp

# Utilites
ix, iy, iz = 0, 1, 2  # xyz indicies, avoid magic numbers
control_net_shown = True  # True lets control net be drawn, False skips it
control_points_shown = True

# The first and only figure
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

# Common to all Bspline surfaces used herein
kv_t = (0.0, 0.0, 0.0, 1.0, 1.0, 1.0)  # knot vector for t parameter
kv_u = (0.0, 0.0, 0.0, 1.0, 1.0, 1.0)  # knot vector for u parameter
degree_t = 2  # quadratic
degree_u = 2  # quadratic
nbi = 2  # number of bisections per knot interval

# Compose collection of Bspline surfaces as a group of control_points that describe
# each surface.
xneg0 = (
    ((0.0, 0.0, 0.0), (0.0, 0.0, 0.5), (0.0, 0.0, 1.0)),
    ((0.0, 0.5, 0.0), (0.0, 0.5, 0.5), (0.0, 0.5, 1.0)),
    ((0.0, 1.0, 0.0), (0.0, 1.0, 0.5), (0.0, 1.0, 1.0)),
)

xneg2 = (
    ((2.0, 0.0, 0.0), (2.0, 0.0, 0.5), (2.0, 0.0, 1.0)),
    ((2.0, 0.25, 0.0), (2.0, 0.75 / 2.0, 0.5), (2.0, 0.5, 1.0)),
    ((2.0, 0.50, 0.0), (2.0, 1.50 / 2.0, 0.5), (2.0, 1.0, 1.0)),
)

xneg4 = (
    ((4.0, 0.0, 0.0), (4.0, 0.0, 0.5), (4.0, 0.0, 1.0)),
    ((4.0, 0.0, 0.0), (4.0, 0.25, 0.5), (4.0, 0.5, 1.0)),
    ((4.0, 0.0, 0.0), (4.0, 0.5, 0.5), (4.0, 1.0, 1.0)),
)

surfaces = (xneg0, xneg2, xneg4)

if control_net_shown:
    pass

if control_points_shown:
    cp_x = np.array(surfaces)[:, :, :, ix].flatten()  # control points x-coordinates
    cp_y = np.array(surfaces)[:, :, :, iy].flatten()  # control points y-coordinates
    cp_z = np.array(surfaces)[:, :, :, iz].flatten()  # control points z-coordinates

    ax.plot3D(cp_x, cp_y, cp_z, **vbsp.defaults["control_points_kwargs"])

for control_points in surfaces:
    S = bsp.Surface(
        kv_t, kv_u, control_points, degree_t, degree_u, n_bisections=nbi, verbose=True,
    )
    (surf_x, surf_y, surf_z) = S.evaluations

    ax.plot3D(
        surf_x.flatten(),
        surf_y.flatten(),
        surf_z.flatten(),
        **vbsp.defaults["evaluation_points_kwargs"]
    )

    u, t = np.meshgrid(S.evaluation_times_u, S.evaluation_times_t)
    u, t = u.flatten(), t.flatten()
    tri = mtri.Triangulation(u, t)

    triangulation_kwargs = dict(triangles=tri.triangles)
    triangulation_kwargs.update(**vbsp.defaults["surface_kwargs"])

    current_color_kwargs = dict(color=vbsp.colors[0])
    triangulation_kwargs.update(current_color_kwargs)

    ax.plot_trisurf(
        surf_x.flatten(), surf_y.flatten(), surf_z.flatten(), **triangulation_kwargs
    )

# Back to the singleton figure
plt.show()
