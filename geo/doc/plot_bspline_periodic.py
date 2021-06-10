"""This module tests creation of an eight-sided ring composed of eight linear
periodic basis functions (p=1), composed of nine knots.

Example (interactive):
> cd ~/sibl/geo/tests
> conda activate siblenv
> python plot_bspline_periodic.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import MultipleLocator
from pathlib import Path

import ptg.bspline_periodic as bspp

display = True
dpi = 100  # dots per inch
latex = False
n_bisections = 3  # 2^3 = 8 intervals
serialize = False

colors = ("tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:cyan")
linestyles = ("solid", "dashed", "dashdot")

if latex:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)

degree = 1  # linear
# degree = 2  # quadratic

local_path = "~/sibl/geo/data/bezier/circle-points.csv"
a = Path(local_path)
b = a.expanduser()
c = str(b)

x, y, z = bspp.bspline_periodic(
    control_points_file=c,
    verbose=True,
    degree=1,
    n_bisections=1,
)

fig = plt.figure()
ax = fig.gca()

_eps = 0.1
ax.set_xlim([0.0 - 2 * _eps, 1.0 + 2 * _eps])
ax.set_ylim([0.0 - 2 * _eps, 1.0 + 2 * _eps])

ax.set_aspect("equal")

ax.xaxis.set_major_locator(MultipleLocator(1.0))
ax.xaxis.set_minor_locator(MultipleLocator(0.25))
ax.yaxis.set_major_locator(MultipleLocator(1.0))
ax.yaxis.set_minor_locator(MultipleLocator(0.25))

if display:
    plt.show()

if serialize:
    extension = ".pdf"  # or '.svg'
    bstring = Path(__file__).stem + extension
    # fig.savefig(bstring, bbox_inches="tight")
    fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
