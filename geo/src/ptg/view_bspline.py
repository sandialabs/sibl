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

    @staticmethod
    def create(config_file, verbose: bool = True):

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
        for item in config_schema:
            value = kwargs.get(item, None)
            if not value:
                sys.exit(f'Error: keyword "{item}" not found in config input file.')

        FACTORY_ITEMS = {"basis": ViewBSplineBasis, "curve": ViewBSplineCurve}

        # config parameters without defaults, user specification required
        CLASS = kwargs.get("class")

        if CLASS in FACTORY_ITEMS:
            # create the class instance
            instance = FACTORY_ITEMS.get(CLASS, None)
            if instance:
                return instance(**kwargs)

        else:
            print(f"Error: 'class': '{CLASS}' is not in the FACTORY_ITEMS dictionary.")
            print("Available 'key': 'value' FACTORY_ITEMS are:")
            for item in FACTORY_ITEMS:
                print(f"   'class': '{item}'")
            sys.exit()


class ViewBSplineBase(ABC):
    """Abstract base class for ViewBSpline classes"""

    def __init__(self, **kwargs):
        z = 4
        # factory has already checked items are specified, no default values necessary
        self.DEGREE = kwargs.get("degree")  # 0 constant, 1 linear, 2 quadratic, etc.
        self.NAME = kwargs.get("name")  # name is used for output file name
        self.NCP = kwargs.get("ncp")

        # get config specification, specify defaults otherwise
        self.DISPLAY = kwargs.get("display", True)  # show figure to screen
        self.DPI = kwargs.get("dpi", 100)  # dots per inch

        _KNOT_OFFSET = kwargs.get(
            "knot_offset", 0
        )  # translate knot vector to left or right

        _a, _b = 0, self.NCP - self.DEGREE
        _knot_vector_default = (
            np.concatenate(
                (
                    np.repeat(_a, self.DEGREE),
                    np.arange(_a, _b),
                    np.repeat(_b, self.DEGREE + 1),
                )
            )
            + _KNOT_OFFSET
        )
        self.KV = kwargs.get(
            "knot_vector", _knot_vector_default
        )  # default is open knot vector, no internal knot multiplicity

        self.LATEX = kwargs.get("latex", False)  # use LaTeX instead of default fonts
        self.LS = kwargs.get("linestyles", ("solid", "dashed", "dashdot"))  # linestyles

        if self.LATEX:
            rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
            rc("text", usetex=True)

        # number of elements is the number of non-zero knot spans
        self.NEL = len(np.unique(self.KV)) - 1
        self.NBI = kwargs.get("nbi", 2)  # number of bisections per knot interval

        self.SERIALIZE = kwargs.get("serialize", False)  # save figure to disc
        self.XTICKS = kwargs.get("xticks", None)
        self.YTICKS = kwargs.get("yticks", None)

        print(f"Computing B-spline basis with degree={self.DEGREE}")
        print(f"with knot vector {self.KV}")
        print(f"of {len(self.KV)} knots")
        print(f"with number of bisections per knot interval={self.NBI}")
        print(f"with number of elements (non-zero knot spans)={self.NEL}")

        _knots_lhs = self.KV[0:-1]  # left-hand-side knot values
        _knots_rhs = self.KV[1:]  # right-hand-side knot values
        _knot_spans = np.array(_knots_rhs) - np.array(_knots_lhs)
        _dt = _knot_spans / (2 ** self.NBI)
        assert all([dti >= 0 for dti in _dt]), "Error: knot vector is decreasing."

        _num_knots = len(self.KV)
        _t = [
            _knots_lhs[k] + j * _dt[k]
            for k in np.arange(_num_knots - 1)
            for j in np.arange(2 ** self.NBI)
        ]
        _t.append(self.KV[-1])  # evauation times
        self.T = np.array(_t)  # recast as numpy array
        self.N = []  # B-spline basis vector at evaluation times
        self.C = []  # B-spline curve at evaluation times


class ViewBSplineBasis(ViewBSplineBase):
    """Creates a Matplotlib figure of BSpline basis functions."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        COEF = kwargs.get(
            "coefficients", None
        )  # None is basis, not None is curve, surface, or volume
        assert COEF is None

        # build up B-spline basis functions
        for i in np.arange(self.NCP):

            coef = np.zeros(self.NCP)
            coef[i] = 1.0

            _B = bsp.BSpline(self.KV, coef, self.DEGREE)

            if _B.is_valid():
                _y = _B.evaluate(self.T)
                self.N.append(_y)

        # plot B-spline basis functions
        self.fig = plt.figure(figsize=plt.figaspect(1.0 / (self.NEL + 1)), dpi=self.DPI)
        ax = self.fig.gca()

        # loop over each basis function and plot it
        for i in np.arange(self.NCP):
            _CPTXT = f"{i}"
            _DEGTXT = f"{self.DEGREE}"
            ax.plot(
                self.T,
                self.N[i],
                "-",
                lw=2,
                label="$N_{" + _CPTXT + "}^{" + _DEGTXT + "}$",
                linestyle=self.LS[np.remainder(i, len(self.LS))],
            )

        ax.set_xlabel(r"$t$")
        ax.set_ylabel(f"$N^{self.DEGREE}_i(t)$")

        _eps = 0.1
        ax.set_xlim([self.KV[0] - 2 * _eps, self.KV[-1] + 2 * _eps])
        ax.set_ylim([0.0 - 2 * _eps, 1.0 + 2 * _eps])

        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

        ax.xaxis.set_major_locator(MultipleLocator(1.0))
        ax.xaxis.set_minor_locator(MultipleLocator(0.25))
        ax.yaxis.set_major_locator(MultipleLocator(1.0))
        ax.yaxis.set_minor_locator(MultipleLocator(0.25))

        # finish figure by calling method with common figure functions
        ViewBSplineFigure(self)


class ViewBSplineCurve(ViewBSplineBase):
    """Creates a Matplotlib figure of BSpline curve."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        COEF = kwargs.get(
            "coefficients", None
        )  # None is basis, not None is curve, surface, or volume
        assert COEF is not None

        # build up B-spline basis functions, multiplied by coefficients
        _NSD = len(COEF[0])  # number of space dimensions
        assert _NSD == 2  # only 2D curves implemented for now, do 3D later

        for i in np.arange(_NSD):

            coef = np.array(COEF)[:, i]

            _B = bsp.BSpline(self.KV, coef, self.DEGREE)

            if _B.is_valid():
                _y = _B.evaluate(self.T)
                self.C.append(_y)

        # plot B-spline curve, assume 2D for now
        self.fig = plt.figure(dpi=self.DPI)
        ax = self.fig.gca()

        ax.plot(self.C[0], self.C[1], color="navy", linestyle="solid", linewidth=2)

        _cp_x = np.array(COEF)[:, 0]  # control points x-coordinates
        _cp_y = np.array(COEF)[:, 1]  # control points y-coordinates

        ax.plot(
            _cp_x,
            _cp_y,
            color="red",
            linewidth=1,
            alpha=0.5,
            marker="o",
            markerfacecolor="white",
            linestyle="dashed",
        )
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")

        # finish figure by calling method with common figure functions
        ViewBSplineFigure(self)


class ViewBSplineFigure:
    def __init__(self, ViewBSplineBase):
        base = ViewBSplineBase
        ax = base.fig.gca()
        ax.set_aspect("equal")
        ax.grid(True, which="major", linestyle="-")
        ax.grid(True, which="minor", linestyle=":")
        # ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

        if base.XTICKS:
            ax.set_xticks(base.XTICKS)

        if base.YTICKS:
            ax.set_yticks(base.YTICKS)

        if base.DISPLAY:
            plt.show()

        if base.SERIALIZE:
            extension = ".pdf"  # or '.svg'
            if base.NAME is None:
                filename = (
                    "N(p=" + str(base.DEGREE) + ")_NCP=" + str(base.NCP) + extension
                )
            else:
                filename = base.NAME + extension
            base.fig.savefig(filename, bbox_inches="tight", pad_inches=0)
            print(f"Serialized file to {filename}")


# class ViewBSplineSurface(ViewBSplineBase):
# TODO

# class ViewBSplineVolume(ViewBSplineBase):
# TODO


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
