"""This module tests creation of an eight-sided ring composed of eight linear
periodic basis functions (p=1), composed of nine knots.

Example (test):
> cd ~/sibl/geo/tests
> conda activate siblenv
> pytest test_bspline_fit_linear_ring.py

Example (interactive):
> cd ~/sibl/geo/tests
> conda activate siblenv
> python test_bspline_fit_linear_ring.py
"""

import numpy as np
import matplotlib.pyplot as plt

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

ax.set_aspect("equal")

ax.xaxis.set_major_locator(MultipleLocator(1.0))
ax.xaxis.set_minor_locator(MultipleLocator(0.25))
ax.yaxis.set_major_locator(MultipleLocator(1.0))
ax.yaxis.set_minor_locator(MultipleLocator(0.25))

if display:
    plt.show()

if serialize:
    extension = ".pdf"  # or '.svg'
    bstring = "bspline_fit_linear_ring" + extension
    # fig.savefig(bstring, bbox_inches="tight")
    fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
