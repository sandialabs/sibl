from abc import ABC
import argparse
import json
from pathlib import Path
import sys

# from matplotlib.ticker import AutoMinorLocator
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import MultipleLocator
import numpy as np

import ptg.bspline as bsp

"""
$ conda active siblenv
$ python view_bspline.py model_config.json
e.g.
$ python view_bspline.py ../../data/bspline/recover_bezier_linear.json
$ python view_bspline.py ../../data/bspline/recover_bezier_linear.json --verbose
"""


class ViewBSplineFactory:
    """The one and only (singleton) factory for ViewBSpline objects."""

    # def __init__(self, config, verbose=True):
    @staticmethod
    def create(config_file, verbose=True):
        # def __init__(self, config, verbose=True):

        # abbreviations:
        # cp: control point; collection of control points forms the control net
        # cn: control net, composed of control points
        # n_cp: number of control points (int) per net
        # n_nets: number of control nets (int)

        if not Path(config_file).is_file():
            sys.exit(f"Error: cannot find file {config_file}")

        STEM = Path(config_file).stem

        config_path = Path(config_file).parent

        if verbose:
            # class_name = type(self).__name__
            class_name = ViewBSplineFactory.__name__
            print(f"This is {class_name}:")
            print(f"  processing config file: {config_file}")
            print(f"  located at: {config_path}")

        with open(config_file) as fin:
            kwargs = json.load(fin)

        # config parameters without defaults, user specification required
        config_schema = (
            "class",
            "degree",
            "name",
            "ncp",
        )

        # check .json input schema
        for key in config_schema:
            value = kwargs.get(key, None)
            if not value:
                sys.exit(f'Error: keyword "{key}" not found in config input file.')

        FACTORY_ITEMS = {"basis": ViewBSplineBasis, "curve": ViewBSplineCurve}

        # config parameters without defaults, user specification required
        CLASS = kwargs.get("class")

        if CLASS in FACTORY_ITEMS:
            a = 4
            # create the class instance

            # "Main factory method, returns XY objects."
            instance = FACTORY_ITEMS.get(CLASS, None)
            if instance:
                # return instance(db)
                # a = instance(db)
                a = instance(**kwargs)

        else:
            print(
                f"Error: class '{CLASS}' is not in the FACTORY_ITEMS dictionary '{FACTORY_ITEMS}'."
            )
            sys.exit()

        # model_module = import_module(f'{k}.model')
        # model_class = getattr(model_module, 'Model')
        # models.append(model_class(**v))

        # DEGREE = db.get("degree")  # 0 constant, 1 linear, 2 quadratic, 3 cubic
        # NAME = db.get("name")  # name is used for output file name
        # NCP = db.get("ncp")  # number of control points, later divine this

        # config parameters with defaults, overwrite if they exist from the input file
        DISPLAY = db.get("display", True)  # show to screen
        DPI = db.get("dpi", 100)  # dots per inch
        # KNOT_OFFSET = db.get("knot_offset", 0)  # translate knot vector to left or right
        LATEX = db.get("latex", False)  # use LaTeX instead of default fonts
        # NBI = db.get("nbi", 2)  # number of bisections per knot interval
        # NCP = db.get("ncp", 2)  # number of control points
        SERIALIZE = db.get("serialize", False)  # save figure to disc
        # VERBOSE = db.get("verbose", False)
        XTICKS = db.get("xticks", None)
        YTICKS = db.get("yticks", None)
        COEF = db.get(
            "coefficients", None
        )  # None is basis, not None is curve, surface, or volume

        LS = ("solid", "dashed", "dashdot")  # linestyles
        NLS = len(LS)  # number of linestyles

        if LATEX:
            rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
            rc("text", usetex=True)

        a = 4


class ViewBSplineBase(ABC):
    """Abstract base class for ViewBSpline classes"""

    def __init__(self, **kwargs):
        z = 4
        DEGREE = kwargs.get("degree")

        KNOT_OFFSET = kwargs.get(
            "knot_offset", 0
        )  # translate knot vector to left or right

        NAME = kwargs.get("name")  # name is used for output file name

        NBI = kwargs.get("nbi", 2)  # number of bisections per knot interval
        NCP = kwargs.get("ncp")

        a, b = 0, NCP - DEGREE
        knot_vector = (
            np.concatenate(
                (np.repeat(a, DEGREE), np.arange(a, b), np.repeat(b, DEGREE + 1))
            )
            + KNOT_OFFSET
        )
        KV = kwargs.get(
            "knot_vector", knot_vector
        )  # default is open vector, no internal knot multiplicity


class ViewBSplineBasis(ViewBSplineBase):
    """Creates a Matplotlib figure of BSpline basis functions."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        a = 4


class ViewBSplineCurve(ViewBSplineBase):
    """Creates a Matplotlib figure of BSpline curve."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        a = 4


# class ViewBSplineSurface(ViewBSplineBase):
# class ViewBSplineVolume(ViewBSplineBase):


# NAME = config.get("name", None)  # name is used for output file name
# DEGREE = config.get("degree", 0)  # 0 constant, 1 linear, 2 quadratic, 3 cubic
# DISPLAY = config.get("display", True)  # show to screen
# DPI = config.get("dpi", 100)  # dots per inch
# KNOT_OFFSET = config.get("knot_offset", 0)  # translate knot vector to left or right
# LATEX = config.get("latex", False)  # use LaTeX instead of default fonts
# NBI = config.get("nbi", 2)  # number of bisections per knot interval
# NCP = config.get("ncp", 2)  # number of control points
# SERIALIZE = config.get("serialize", False)  # save figure to disc
# VERBOSE = config.get("verbose", False)
# XTICKS = config.get("xticks", None)
# YTICKS = config.get("yticks", None)
# COEF = config.get("coefficients", None)  # None is basis, not None is curve
#
# linestyles = ["solid", "dashed", "dashdot"]
# num_linestyles = len(linestyles)
#
# if LATEX:
#     rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
#     rc("text", usetex=True)
#
# a, b = 0, NCP - DEGREE
# knot_vector = (
#     np.concatenate((np.repeat(a, DEGREE), np.arange(a, b), np.repeat(b, DEGREE + 1)))
#     + KNOT_OFFSET
# )
# KV = config.get(
#     "knot_vector", knot_vector
# )  # default is open vector, no internal knot multiplicity
#
# # number of elements is the number of non-zero knot spans
# num_elements = len(np.unique(KV)) - 1
#
# print(f"Computing B-spline basis with degree={DEGREE}")
# print(f"with knot vector {KV}")
# print(f"of {len(KV)} knots")
# print(f"with number of bisections per knot interval={NBI}")
# print(f"with number of elements (non-zero knot spans)={num_elements}")
#
# knots_lhs = KV[0:-1]  # left-hand-side knot values
# knots_rhs = KV[1:]  # right-hand-side knot values
# knot_spans = np.array(knots_rhs) - np.array(knots_lhs)
# dt = knot_spans / (2 ** NBI)
# assert all([dti >= 0 for dti in dt]), "Error: knot vector is decreasing."
#
# num_knots = len(KV)
# t = [
#     knots_lhs[k] + j * dt[k]
#     for k in np.arange(num_knots - 1)
#     for j in np.arange(2 ** NBI)
# ]
# t.append(KV[-1])
# t = np.array(t)
# N = []  # B-spline basis vector
# C = []  # B-spline curve
#
# if not COEF:
#     # plot B-spline basis
#     for i in np.arange(NCP):
#
#         coef = np.zeros(NCP)
#         coef[i] = 1.0
#
#         B = bsp.BSpline(KV, coef, DEGREE)
#
#         if B.is_valid():
#             y = B.evaluate(t)
#             N.append(y)
# else:
#     # plot B-spline curve
#     nsd = len(COEF[0])  # number of space dimensions
#     for i in np.arange(nsd):
#         coef = np.array(COEF)[:, i]
#         # coef = COEF[:, i]
#
#         B = bsp.BSpline(KV, coef, DEGREE)
#
#         if B.is_valid():
#             y = B.evaluate(t)
#             C.append(y)
#
#
# # fig = plt.figure(figsize=plt.figaspect(1.0 / (num_knots - 1)), dpi=DPI)
# fig = plt.figure(figsize=plt.figaspect(1.0 / (num_elements + 1)), dpi=DPI)
# ax = fig.gca()
# # ax.grid()
# # ax.grid(True, which="both")  # both major and minor grid to on
# ax.grid(True, which="major", linestyle="-")
# ax.grid(True, which="minor", linestyle=":")
#
# if not COEF:
#     # plot B-spline basis
#     for i in np.arange(NCP):
#         CPTXT = f"{i}"
#         DEGTXT = f"{DEGREE}"
#         ax.plot(
#             t,
#             N[i],
#             "-",
#             lw=2,
#             label="$N_{" + CPTXT + "}^{" + DEGTXT + "}$",
#             linestyle=linestyles[np.remainder(i, num_linestyles)],
#         )
#         ax.set_xlabel(r"$t$")
#         ax.set_ylabel(f"$N^{DEGREE}_i(t)$")
#         eps = 0.1
#         ax.set_xlim([KV[0] - 2 * eps, KV[-1] + 2 * eps])
#         ax.set_ylim([0.0 - 2 * eps, 1.0 + 2 * eps])
#         ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
#         ax.xaxis.set_major_locator(MultipleLocator(1.0))
#         ax.xaxis.set_minor_locator(MultipleLocator(0.25))
#         ax.yaxis.set_major_locator(MultipleLocator(1.0))
#         ax.yaxis.set_minor_locator(MultipleLocator(0.25))
# else:
#     # plot B-spline curve, assume 2D for now
#     ax.plot(C[0], C[1], color="navy", linestyle="solid", linewidth=2)
#     cp_x = np.array(COEF)[:, 0]
#     cp_y = np.array(COEF)[:, 1]
#     ax.plot(
#         cp_x,
#         cp_y,
#         color="red",
#         linewidth=1,
#         alpha=0.5,
#         marker="o",
#         markerfacecolor="white",
#         linestyle="dashed",
#     )
#     ax.set_xlabel(r"$x$")
#     ax.set_ylabel(r"$y$")
#     # ax.xaxis.set_major_locator(MultipleLocator(0.1))
#     # ax.xaxis.set_minor_locator(MultipleLocator(0.25))
#     # ax.yaxis.set_major_locator(MultipleLocator(0.1))
#     # ax.yaxis.set_minor_locator(MultipleLocator(0.25))
#
# ax.set_aspect("equal")
# # ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
#
# if XTICKS:
#     ax.set_xticks(XTICKS)
#
# if YTICKS:
#     ax.set_yticks(YTICKS)
#
# if DISPLAY:
#     plt.show()
#
# if SERIALIZE:
#     extension = ".pdf"  # or '.svg'
#     # bstring = "N(p=" + str(DEGREE) + ")_" + str(k) + extension
#     if NAME is None:
#         bstring = "N(p=" + str(DEGREE) + ")_NCP=" + str(NCP) + extension
#     else:
#         bstring = NAME + extension
#     # fig.savefig(bstring, bbox_inches="tight")
#     fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
#     print(f"Serialized file to {bstring}")


def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "config_file", help=".json BSpline basis, curve, surface, volume specification"
    )

    parser.add_argument(
        "--verbose", help="increased command line feedback", action="store_true"
    )

    args = parser.parse_args()

    config_file = args.config_file
    verbose = args.verbose

    # ViewBSplineFactory.create(config, verbose)
    item = ViewBSplineFactory.create(config_file, verbose)
    # ViewBSplineBasis(config)
    a = 4


if __name__ == "__main__":
    main(sys.argv[1:])
