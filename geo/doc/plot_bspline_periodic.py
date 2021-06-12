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

colors = (
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple",
    "tab:brown",
    "tab:pink",
    "tab:gray",
    "tab:olive",
    "tab:cyan",
)
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
    degree=2,
    n_bisections=2,
)

fig = plt.figure()
ax = fig.gca()
# ax.grid()
ax.grid(True, which="major", linestyle="-")
ax.grid(True, which="minor", linestyle=":")

# offset for element labels
ox, oy = 0.1, 0.1

for i in np.arange(len(x)):
    # for i in np.arange(1):
    print(f"element {i+1}")
    color = colors[np.remainder(i, len(colors))]
    ax.plot(
        x[i],
        y[i],
        "-o",
        linewidth=2,
        # color=colors[np.remainder(i, len(colors))],
        color=color,
        linestyle=linestyles[np.remainder(i, len(linestyles))],
    )
    # draw in elements as an element number with a circle
    ax.annotate(
        str(i),
        xy=(np.average(x[i]) + ox, np.average(y[i]) + oy),
        xycoords="data",
        bbox={"boxstyle": "circle", "color": color, "alpha": 0.2},
        horizontalalignment="center",
        verticalalignment="center",
    )
    a = 4

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
# ax.legend(loc="upper right")

_eps = 0.1
ax.set_xlim([-1.0 - 2 * _eps, 1.0 + 2 * _eps])
ax.set_ylim([-1.0 - 2 * _eps, 1.0 + 2 * _eps])

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
