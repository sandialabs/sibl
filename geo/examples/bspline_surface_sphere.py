"""
Example:
> cd ~/sibl/geo/examples
> conda activate siblenv
> python bspline_surface_sphere.py
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

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
ax.set_zlabel(r"$z$")

xmax = 3
ax.set_xlim([0, xmax])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])

ax.set_box_aspect([2.5, 1, 1])

interval = np.arange(0, xmax + 1, 1)

ax.set_xticks(interval)
ax.set_yticks([-1, 0, 1])
ax.set_zticks([0, 1])

# Common to all Bspline scaffolds used herein
kv_p2 = (0.0, 0.0, 0.0, 1.0, 1.0, 1.0)  # knot vector for t, u parameter
kv_p2ext = (0.0, 0.0, 0.0, 1.0, 2.0, 2.0, 2.0)  # knot insertion, for t, u parameter
quadratic = 2  # quadratic
# degree_cubic = 3  # quadratic
nbi = 4  # number of bisections per knot interval

# Compose collection of Bspline scaffolds as a group of control_points that describe
# each surface.

cyl0 = (
    ((0.0, 0.5, 0.0), (0.0, 0.5, 0.5), (0.0, 0.0, 0.5)),
    ((0.5, 1.0, 0.0), (0.5, 1.0, 1.0), (0.5, 0.0, 1.0)),
    ((1.0, 0.5, 0.0), (1.0, 0.5, 0.5), (1.0, 0.0, 0.5)),
)

cyl0b = (
    ((0.0, -0.5, 0.0), (0.0, -0.5, 0.5), (0.0, 0.0, 0.5)),
    ((0.5, -1.0, 0.0), (0.5, -1.0, 1.0), (0.5, 0.0, 1.0)),
    ((1.0, -0.5, 0.0), (1.0, -0.5, 0.5), (1.0, 0.0, 0.5)),
)

cyl2 = (
    ((2.0, 0.0, 0.0), (2.0, 0.0, 0.0), (2.0, 0.0, 0.0)),
    ((2.5, 1.0, 0.0), (2.5, 1.0, 1.0), (2.5, 0.0, 1.0)),
    ((3.0, 0.0, 0.0), (3.0, 0.0, 0.0), (3.0, 0.0, 0.0)),
)

# knot insertion
# To come.

# collect as scaffolds (formerly called "surfaces", which is not precise)
scaffolds = (cyl0, cyl0b, cyl2)
kvs = (kv_p2, kv_p2, kv_p2)  # knot vectors

# consider refactor into a Generator, e.g. snrl ref itertools.tee

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
