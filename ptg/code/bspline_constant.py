import numpy as np
import matplotlib.pyplot as plt

# from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc

# from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator

import bspline_polynomial as bp

DISPLAY = 1
DPI = 100  # dots per inch
LATEX = 1
SERIALIZE = 1
VERBOSE = 0

if LATEX:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)

p_degree = 0  # e.g., p=0 constant, p=1 linear, p=2 quadratic, p=3 cubic

# number of time intervals per knot
# nti = 2 ** 1  # for minimal interpolation
nti = 2 ** 5  # for LaTeX figures

# knot_vector = [0, 1, 2]
knot_vector = [0, 1, 2, 3, 4, 5, 6]

print(f"Computing B-spline bases with degree p={p_degree}")
print(f"with knot vector {knot_vector} and ")
print(f"with number of time intervals (per knot span) nti={nti}")

for k in np.arange(len(knot_vector) - 1):

    t, y = bp.bspline_polynomial(knot_vector, k, p_degree, nti, VERBOSE)

    if VERBOSE:
        print(f"t={t}")
        print(f"y = {y}")

    # fig = plt.figure(figsize=plt.figaspect(1.0), dpi=DPI)
    # fig = plt.figure(dpi=DPI)
    fig = plt.figure(figsize=plt.figaspect(1.0 / (len(knot_vector) - 1)), dpi=DPI)
    ax = fig.gca()
    ax.grid()
    # ax.scatter(t, y)
    ax.plot(t, y, linestyle="None", marker=".")

    # if k == len(knot_vector) - 2:
    if k in [2, 5]:  # plot three per page, over two pages
        # stack all figures in documentation, x-axis only on
        # last figure, which will be on the bottom of the stack
        ax.set_xlabel(r"$t$")
    else:
        # suppress x-ticks except for on the bottom plot
        plt.setp(ax.get_xticklabels(), visible=False)

    ax.set_ylabel(r"$N^{" + str(p_degree) + "}_{" + str(k) + "}(t)$")

    eps = 0.1
    ax.set_xlim([knot_vector[0] - 2 * eps, knot_vector[-1] + 2 * eps])
    ax.set_ylim([0 - 2 * eps, 1 + 2 * eps])
    ax.set_aspect("equal")
    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))

    if DISPLAY:
        plt.show()

    if SERIALIZE:
        extension = ".pdf"  # or '.svg'
        bstring = "N(p=" + str(p_degree) + ")_" + str(k) + extension
        # fig.savefig(bstring, bbox_inches="tight")
        fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
