import numpy as np
import matplotlib.pyplot as plt

# from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc

# from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator

import bernstein_polynomial as bp

DISPLAY = 1
DPI = 100  # dots per inch
LATEX = 0
SERIALIZE = 0
VERBOSE = 1
Z_AXIS_LABEL_INVERTED = 1

if LATEX:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)

p_degree = 1  # e.g., p=1 linear, p=2 quadratic, p=3 cubic
cp_t = np.arange(p_degree + 1)  # control points in the t direction
cp_u = np.arange(p_degree + 1)  # control points in the u direction

# control points in (t, u) space
cp_tu = tuple((i, j) for i in cp_t for j in cp_u)
cp_ts = [z[0] / p_degree for z in cp_tu]
cp_us = [z[1] / p_degree for z in cp_tu]
cp_bs = [0 for z in cp_tu]  # plot control points at zero for the B axis

# number of time intervals
# e.g., 4 time intervals implies 5 evaluation points along an axis, t or u
# nti = 2 ** 1  # for minimal interpolation
nti = 2 ** 5  # for LaTeX figures
# azimuth, elevation = (-15, 15)  # degrees
azimuth, elevation = (15, 15)  # degrees
# azimuth, elevation = (-75, 15)  # degrees

bases = np.array([np.array([])])

print(f"Computing Bezier surface with degree p={p_degree}")
print(f"with number of time intervals nti={nti}")

for i in cp_t:
    for j in cp_u:

        b_i = bp.bernstein_polynomial(i, p_degree, nti)
        b_j = bp.bernstein_polynomial(j, p_degree, nti)
        bij = np.outer(b_i, b_j)
        if VERBOSE:
            print(f"i={i}, j={j}")
            print(f"bij = {bij}")

        # fig = plt.figure()
        fig = plt.figure(figsize=plt.figaspect(1.0), dpi=DPI)
        # fig = plt.figure(figsize=(6.5, 3.25), dpi=DPI)
        ax = fig.gca(projection="3d")
        ax.view_init(elevation, azimuth)
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        t = np.linspace(0, 1, nti + 1)
        # for projecting onto [t, B] and [u, B] planes
        zeros = [0 for i in range(len(t))]

        # on the (t, u) grid:
        tij = np.outer(t, np.ones(nti + 1))  # all of the t values from [0, 1]
        uij = np.outer(np.ones(nti + 1), t)  # all of the u values from [0, 1]
        if VERBOSE:
            print(f"tij = {tij}")
            print(f"uij = {uij}")

        # plot the control net in the [t, u] plane
        ax.scatter3D(cp_ts, cp_us, cp_bs, edgecolor="black", facecolor="black", s=20)

        # plot the Bezier basis functions in the [u, B] plane
        for II in cp_t:
            ax.plot3D(
                t,
                zeros,
                bp.bernstein_polynomial(II, p_degree, nti),
                color="gray",
                linewidth=0.5,
            )

        # and highlight the current basis function
        ax.plot3D(
            t,
            zeros,
            bp.bernstein_polynomial(i, p_degree, nti),
            color="red",
            linewidth=1.5,
        )

        # plot the Bezier basis functions in the [t, B] plane
        for JJ in cp_u:
            ax.plot3D(
                zeros,
                t,
                bp.bernstein_polynomial(JJ, p_degree, nti),
                color="gray",
                linewidth=0.5,
            )

        # and highlight the current basis function
        ax.plot3D(
            zeros,
            t,
            bp.bernstein_polynomial(j, p_degree, nti),
            color="green",
            linewidth=1.5,
        )

        surf = ax.plot_surface(tij, uij, bij, alpha=0.8)

        ax.set_xlabel(r"$t$")
        ax.set_ylabel(r"$u$")
        ax.set_zlabel(
            r"$B^{" + str(p_degree) + "}_{" + str(i) + ", " + str(j) + "}(t, u)$"
        )
        if Z_AXIS_LABEL_INVERTED:
            ax.zaxis.set_rotate_label(False)
            ax.zaxis.label.set_rotation(90)

        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_zlim([0, 1])
        ax.xaxis.set_major_locator(MultipleLocator(0.25))
        ax.yaxis.set_major_locator(MultipleLocator(0.25))
        ax.zaxis.set_major_locator(MultipleLocator(0.25))

        if DISPLAY:
            plt.show()

        if SERIALIZE:
            extension = ".pdf"  # or '.svg'
            bstring = "B(p=" + str(p_degree) + ")_" + str(i) + "_"
            bstring += str(j) + extension
            # fig.savefig(bstring, bbox_inches="tight")
            fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
