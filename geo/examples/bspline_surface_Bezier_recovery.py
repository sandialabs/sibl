"""This module recovers the Bezier bilinear B00_p1_surface.
    See also `test_201_recover_bezier_bilinear_B00_p1_surface.py`

Example:
> cd ~/sibl/geo/examples
> conda activate siblenv
> python bspline_surface_Bezier_recovery.py
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
serialize = True
latex = True
if latex:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)

# The first and only figure
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r"$z$")

xmin, nsamples, xmax = 0.0, 5, 1.0
interval = np.linspace(xmin, xmax, num=nsamples, endpoint=True)

ax.set_xticks(interval)
ax.set_yticks(interval)
ax.set_zticks(interval)

# The first and only Bspline surface
kv_t = (0.0, 0.0, 1.0, 1.0)  # knot vector for t parameter
kv_u = (0.0, 0.0, 1.0, 1.0)  # knot vector for u parameter
degree_t = 1  # linear
degree_u = 1  # linear
nbi = 3  # number of bisections per knot interval

control_points = (
    ((0.0, 0.0, 1.0), (0.0, 1.0, 0.0)),
    ((1.0, 0.0, 0.0), (1.0, 1.0, 0.0)),
)

surfaces = (control_points,)

if control_net_shown:
    pass

if control_points_shown:
    cp_x = np.array(surfaces)[:, :, :, ix].flatten()  # control points x-coordinates
    cp_y = np.array(surfaces)[:, :, :, iy].flatten()  # control points y-coordinates
    cp_z = np.array(surfaces)[:, :, :, iz].flatten()  # control points z-coordinates

    ax.plot3D(cp_x, cp_y, cp_z, **vbsp.defaults["control_points_kwargs"])

for control_points, surface_color in zip(surfaces, vbsp.colors):

    S = bsp.Surface(
        kv_t,
        kv_u,
        control_points,
        degree_t,
        degree_u,
        n_bisections=nbi,
        verbose=True,
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

    current_color_kwargs = dict(color=surface_color)
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
