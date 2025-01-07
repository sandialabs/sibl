"""This module tests creation of an eight-element ring generated from
periodic modified (linear or quadratic) Bezier basis functions.

Example (interactive):
> cd ~/sibl/geo/doc
> conda activate siblenv
> python plot_modified_bezier.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import MultipleLocator
from pathlib import Path

import ptg.modified_bezier as mb

# client input begin

display = True
dpi = 100  # dots per inch
latex = False
serialize = False

data = "~/sibl/geo/data/bezier/circle-points.csv"
x_min, x_max = -1, 1
y_min, y_max = -1, 1
# data = "~/sibl/geo/data/bezier/sin_1_Hz_10_samples.csv"
# x_min, x_max = -0.25, 2.25
# y_min, y_max = -1, 1

ox, oy = 0.0, 0.0  # offset for element labels

# client input end

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

# data = "~/sibl/geo/data/bezier/circle-points.csv"
a = Path(data)
b = a.expanduser()
c = str(b)

x, y, z = mb.modified_bezier(
    control_points_file=c,
    verbose=True,
    degree=1,
    n_bisections=5,
)

fig = plt.figure()
ax = fig.gca()
# ax.grid()
ax.grid(True, which="major", linestyle="-")
ax.grid(True, which="minor", linestyle=":")


for i in np.arange(len(x)):
    # for i in np.arange(1):
    print(f"element {i + 1}")
    color = colors[np.remainder(i, len(colors))]
    ax.plot(
        x[i],
        y[i],
        # "-o",
        "-",
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
ax.set_xlim([x_min - 2 * _eps, x_max + 2 * _eps])
ax.set_ylim([y_min - 2 * _eps, y_max + 2 * _eps])

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
    print(f"Serialized file to {bstring}")


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
