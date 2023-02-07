# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


import sys
import numpy as np
import matplotlib.pyplot as plt

# from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rc

# from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator

# import ptg.code.bernstein_polynomial as bp
import ptg.bernstein_polynomial as bp

#  import bernstein_polynomial as bp


class ViewBernsteinSurface:
    """Creates a Matplotlib figures of a Bernstein basis surface
    from outer product of two basis functions.

    $ conda active siblenv
    $ python view_bernstein_surface.py
    """

    def __init__(self, config):

        self.INITIALIZED = False

        # get client configuration, or if not specified, set to default configuration
        DEGREE = config.get("degree", 1)
        NTI_BISECTIONS = config.get("number-time-interval-bisections", 1)
        DISPLAY = config.get("display", True)
        AZIMUTH = config.get("camera-azimuth", 15)  # degrees
        ELEVATION = config.get("camera-elevation", 15)  # degrees
        DPI = config.get("dots-per-inch", 100)
        LATEX = config.get("latex", True)
        SERIALIZE = config.get("serialize", True)
        VERBOSE = config.get("verbose", True)
        Z_AXIS_LABEL_INVERTED = config.get("z-axis-label-inverted", True)

        if LATEX:
            rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
            rc("text", usetex=True)

        # DEGREE = 1  # e.g., p=1 linear, p=2 quadratic, p=3 cubic
        cp_t = np.arange(DEGREE + 1)  # control points in the t direction
        cp_u = np.arange(DEGREE + 1)  # control points in the u direction

        # control points in (t, u) space
        cp_tu = tuple((i, j) for i in cp_t for j in cp_u)
        cp_ts = [z[0] / DEGREE for z in cp_tu]
        cp_us = [z[1] / DEGREE for z in cp_tu]
        cp_bs = [0 for z in cp_tu]  # plot control points at zero for the B axis

        # number of time intervals
        # e.g., 4 time intervals implies 5 evaluation points along an axis, t or u
        # nti = 2 ** 1  # for minimal interpolation
        # nti = 2 ** 1  # for LaTeX figures
        nti = 2**NTI_BISECTIONS
        # azimuth, elevation = (-15, 15)  # degrees
        # azimuth, elevation = (15, 15)  # degrees
        # azimuth, elevation = (-75, 15)  # degrees

        # bases = np.array([np.array([])])

        if VERBOSE:
            print(f"Computing Bezier surface with degree p={DEGREE}")
            print(f"with number of time intervals nti={nti}")

        for i in cp_t:
            for j in cp_u:

                b_i = bp.bernstein_polynomial(i, DEGREE, nti)
                b_j = bp.bernstein_polynomial(j, DEGREE, nti)
                bij = np.outer(b_i, b_j)
                if VERBOSE:
                    print(f"i={i}, j={j}")
                    print(f"bij = {bij}")

                # fig = plt.figure()
                fig = plt.figure(figsize=plt.figaspect(1.0), dpi=DPI)
                # fig = plt.figure(figsize=(6.5, 3.25), dpi=DPI)
                #
                # Deprecation warning: keywords no longer allowed with gca() since
                # matplotlib 3.4
                # ax = fig.gca(projection="3d")
                ax = fig.add_subplot(projection="3d")
                #
                # ax.view_init(elevation, azimuth)
                ax.view_init(ELEVATION, AZIMUTH)
                plt.subplots_adjust(
                    left=0, bottom=0, right=1, top=1, wspace=0, hspace=0
                )

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
                ax.scatter3D(
                    cp_ts, cp_us, cp_bs, edgecolor="black", facecolor="black", s=20
                )

                # plot the Bezier basis functions in the [u, B] plane
                for II in cp_t:
                    ax.plot3D(
                        t,
                        zeros,
                        bp.bernstein_polynomial(II, DEGREE, nti),
                        color="gray",
                        linewidth=0.5,
                    )

                # and highlight the current basis function
                ax.plot3D(
                    t,
                    zeros,
                    bp.bernstein_polynomial(i, DEGREE, nti),
                    color="red",
                    linewidth=1.5,
                )

                # plot the Bezier basis functions in the [t, B] plane
                for JJ in cp_u:
                    ax.plot3D(
                        zeros,
                        t,
                        bp.bernstein_polynomial(JJ, DEGREE, nti),
                        color="gray",
                        linewidth=0.5,
                    )

                # and highlight the current basis function
                ax.plot3D(
                    zeros,
                    t,
                    bp.bernstein_polynomial(j, DEGREE, nti),
                    color="green",
                    linewidth=1.5,
                )

                # surf = ax.plot_surface(tij, uij, bij, alpha=0.8)
                ax.plot_surface(tij, uij, bij, alpha=0.8)

                ax.set_xlabel(r"$t$")
                ax.set_ylabel(r"$u$")
                ax.set_zlabel(
                    r"$B^{" + str(DEGREE) + "}_{" + str(i) + ", " + str(j) + "}(t, u)$"
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
                    # plt.show()
                    plt.show(block=False)

                if SERIALIZE:
                    extension = ".pdf"  # or '.svg'
                    bstring = "B(p=" + str(DEGREE) + ")_" + str(i) + "_"
                    bstring += str(j) + extension
                    # fig.savefig(bstring, bbox_inches="tight")
                    fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
                    print(f"Serialized file as {bstring}")

        self.INITIALIZED = True


def main(argv):

    config = {
        "degree": 1,
        "number-time-interval-bisections": 1,
        "display": True,
        "camera-azimuth": 15,
        "camera-elevation": 15,
        "dots-per-inch": 100,
        "latex": True,
        "serialize": False,
        "verbose": True,
        "z-axis-label-inverted": True,
    }

    bs = ViewBernsteinSurface(config)
    result = bs.INITIALIZED
    if result:
        print("Successful initialization and execution.")
    return result


if __name__ == "__main__":
    main(sys.argv[1:])


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
