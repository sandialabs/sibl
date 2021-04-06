"""This module recovers the Bezier bilinear B00_p1_surface.
    See also `test_201_recover_bezier_bilinear_B00_p1_surface.py`

Example:
> cd ~/sibl/geo/examples
> conda activate siblenv
> python bspline_surface_Bezier_recovery.py
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

# The first and only Bspline surface
kv_t = (0.0, 0.0, 1.0, 1.0)  # knot vector for t parameter
kv_u = (0.0, 0.0, 1.0, 1.0)  # knot vector for u parameter
control_points = (
    ((0.0, 0.0, 1.0), (0.0, 1.0, 0.0)),
    ((1.0, 0.0, 0.0), (1.0, 1.0, 0.0)),
)
degree_t = 1  # linear
degree_u = 1  # linear
nbi = 2  # number of bisections per knot interval

S = bsp.Surface(
    kv_t, kv_u, control_points, degree_t, degree_u, n_bisections=nbi, verbose=True,
)
(surf_x, surf_y, surf_z) = S.evaluations

S_evaluations_view_config = dict(
    alpha=0.9, color="navy", linestyle="dashed", linewidth=0, marker=".", markersize=4
)

ax.plot3D(
    surf_x.flatten(), surf_y.flatten(), surf_z.flatten(), **S_evaluations_view_config
)

u, t = np.meshgrid(S.evaluation_times_u, S.evaluation_times_t)
u, t = u.flatten(), t.flatten()
tri = mtri.Triangulation(u, t)
S_triangulation_view_config = dict(alpha=0.8, color="tab:blue", triangles=tri.triangles)
ax.plot_trisurf(
    surf_x.flatten(), surf_y.flatten(), surf_z.flatten(), **S_triangulation_view_config
)

# Back to the singleton figure
plt.show()
