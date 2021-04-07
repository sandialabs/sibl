"""This module recovers a six-sided (bottom, top, lateral) surfaces of a cube.

Example:
> cd ~/sibl/geo/examples
> conda activate siblenv
> python bspline_surface_cube_linear.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

import ptg.bspline as bsp
import ptg.view_bspline as vbsp

# View Control
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
kv_t = (0.0, 0.0, 1.0, 1.0)  # knot vector for t parameter
kv_u = (0.0, 0.0, 1.0, 1.0)  # knot vector for u parameter
degree_t = 1  # linear
degree_u = 1  # linear
nbi = 2  # number of bisections per knot interval

# Compose collection of Bspline surfaces as a group of control_points that describe
# each surface.
xneg = ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0)), ((0.0, 1.0, 0.0), (0.0, 1.0, 1.0))
xpos = ((1.0, 0.0, 0.0), (1.0, 0.0, 1.0)), ((1.0, 1.0, 0.0), (1.0, 1.0, 1.0))

yneg = ((0.0, 0.0, 0.0), (1.0, 0.0, 0.0)), ((0.0, 0.0, 1.0), (1.0, 0.0, 1.0))
ypos = ((0.0, 1.0, 0.0), (1.0, 1.0, 0.0)), ((0.0, 1.0, 1.0), (1.0, 1.0, 1.0))

zneg = ((0.0, 0.0, 0.0), (0.0, 1.0, 0.0)), ((1.0, 0.0, 0.0), (1.0, 1.0, 0.0))
zpos = ((0.0, 0.0, 1.0), (0.0, 1.0, 1.0)), ((1.0, 0.0, 1.0), (1.0, 1.0, 1.0))

# surfaces = (xneg, xpos)
surfaces = (xneg, xpos, yneg, ypos)
# surfaces = (xneg, xpos, yneg, ypos, zneg, zpos)

if control_net_shown:
    pass

if control_points_shown:
    cp_x = np.array(surfaces)[:, :, :, ix].flatten()  # control points x-coordinates
    cp_y = np.array(surfaces)[:, :, :, iy].flatten()  # control points y-coordinates
    cp_z = np.array(surfaces)[:, :, :, iz].flatten()  # control points z-coordinates

    ax.plot3D(cp_x, cp_y, cp_z, **vbsp.defaults["control_points_kwargs"])

for control_points, surface_color in zip(surfaces, vbsp.colors):
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

    current_color_kwargs = dict(color=surface_color)
    triangulation_kwargs.update(current_color_kwargs)

    ax.plot_trisurf(
        surf_x.flatten(), surf_y.flatten(), surf_z.flatten(), **triangulation_kwargs
    )

# Back to the singleton figure
plt.show()
