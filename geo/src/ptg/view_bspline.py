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
import ptg.bspline_fit as bspfit

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
    def create(config: str, verbose: bool = True):
        """Creates a ViewBSpline object that is listed in ViewBSplineFactory.

        Args:
            config (str): .json file name, with path, that specifies dictionary of
                keys and values used to construct ViewBSpline objects.
            verbose (Optional[bool]): True provides feedback during run, False does not.
                Defaults to True.

        Returns:
            A ViewBSplineInstance identified in the factory by the config file.

        """

        if not Path(config).is_file():
            sys.exit(f"Error: cannot find file {config}")

        # _stem = Path(config).stem

        _config_dir = Path(config).parent

        if verbose:
            # _class_name = type(self).__name__
            _class_name = ViewBSplineFactory.__name__
            print(f"This is {_class_name}:")
            print(f"  processing config file: {config}")
            print(f"  located at: {_config_dir}")

        with open(config) as fin:
            kwargs = json.load(fin)

        # config parameters without defaults, user specification required
        # ncp is number of control points, to be replaced by
        # len(control_points) in a future revision
        # _config_schema = (
        #     "class",
        #     "degree",
        #     "name",
        #     "ncp",
        # )
        _config_schema = ("class", "degree", "name")

        # check .json input schema
        for item in _config_schema:
            value = kwargs.get(item, None)
            if not value:
                sys.exit(f'Error: keyword "{item}" not found in config input file.')

        _factory_items = {
            "basis": ViewBSplineBasis,
            "curve": ViewBSplineCurve,
            "curvefit": ViewBSplineCurveFit,
        }

        # config parameters without defaults, user specification required
        _class = kwargs.get("class")

        if _class in _factory_items:
            # create the class instance
            instance = _factory_items.get(_class, None)
            if instance:
                return instance(**kwargs)

        else:
            print(f"Error: No 'class': '{_class}' in the _factory_items dictionary.")
            print("Available 'key': 'value' _factory_items are:")
            for item in _factory_items:
                print(f"   'class': '{item}'")
            sys.exit()


class ViewBase(ABC):
    """Abstract base class for ViewBSpline classes"""

    def __init__(self, **kwargs):
        # factory has already checked items are specified, no default values necessary
        self.DEGREE = kwargs.get("degree")  # 0 constant, 1 linear, 2 quadratic, etc.

        # get config specification, specify defaults otherwise
        self.DISPLAY = kwargs.get("display", True)  # show figure to screen
        self.DPI = kwargs.get("dpi", 100)  # dots per inch

        self.LATEX = kwargs.get("latex", False)  # use LaTeX instead of default fonts
        if self.LATEX:
            rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
            rc("text", usetex=True)
        self.LS = kwargs.get("linestyles", ("solid", "dashed", "dashdot"))  # linestyles

        self.NAME = kwargs.get("name")  # name is used for output file name
        self.NBI = kwargs.get("nbi", 2)  # number of bisections per knot interval

        self.SERIALIZE = kwargs.get("serialize", False)  # save figure to disc

        self.XTICKS = kwargs.get("xticks", None)
        self.YTICKS = kwargs.get("yticks", None)

        self.VERBOSITY = kwargs.get("verbosity", False)


class ViewBSplineBase(ViewBase):
    """Base class for ViewBSplineCurveFit class."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NCP = kwargs.get("ncp")

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

        # number of elements is the number of non-zero knot spans
        self.NEL = len(np.unique(self.KV)) - 1

        print(f"Computing B-spline basis with degree = {self.DEGREE}")
        print(f"  with knot vector {self.KV}")
        print(f"  of {len(self.KV)} knots")
        print(f"  with number of bisections per knot interval = {self.NBI}")
        print(f"  with number of elements (non-zero knot spans) = {self.NEL}")

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
        # self.evaluation_times = np.array(_t)  # recast as numpy array
        self.evaluation_times = np.unique(np.array(_t))  # recast as numpy array
        self.evaluated_bases = []  # B-spline basis vector at evaluation times
        self.evaluated_curve = []  # B-spline curve at evaluation times


class ViewBSplineFitBase(ViewBase):
    """Base class for ViewBSpline Curve, Surface, and Volume classes."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


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
                _y = _B.evaluate(self.evaluation_times)
                self.evaluated_bases.append(_y)

        # plot B-spline basis functions
        self.fig = plt.figure(figsize=plt.figaspect(1.0 / (self.NEL + 1)), dpi=self.DPI)
        ax = self.fig.gca()

        # loop over each basis function and plot it
        for i in np.arange(self.NCP):
            _CPTXT = f"{i}"
            _DEGTXT = f"{self.DEGREE}"
            ax.plot(
                self.evaluation_times,
                self.evaluated_bases[i],
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

        # show/hide control point locations
        _control_points_shown = kwargs.get("control_points_shown", False)

        # show/hide knot locations
        _knots_shown = kwargs.get("knots_shown", False)
        _evaluated_knots = []
        if _knots_shown:
            _knots_t = np.unique(self.KV)

        # show/hide sample points in case of a B-spline fit
        _samples_shown = kwargs.get("samples_shown", False)

        # build up B-spline basis functions, multiplied by coefficients
        _NSD = len(COEF[0])  # number of space dimensions
        assert _NSD == 2  # only 2D curves implemented for now, do 3D later

        for i in np.arange(_NSD):

            coef = np.array(COEF)[:, i]

            _B = bsp.BSpline(self.KV, coef, self.DEGREE)

            if _B.is_valid():
                _y = _B.evaluate(self.evaluation_times)
                self.evaluated_curve.append(_y)

                if _knots_shown:
                    _y = _B.evaluate(_knots_t)
                    _evaluated_knots.append(_y)

        # plot B-spline curve, assume 2D for now
        self.fig = plt.figure(dpi=self.DPI)
        ax = self.fig.gca()

        if _control_points_shown:
            # plot control points
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
                markersize=9,
                linestyle="dashed",
            )

        if _samples_shown:
            _samples_x = np.array(kwargs.get("samples"))[:, 0]
            _samples_y = np.array(kwargs.get("samples"))[:, 1]
            ax.plot(
                _samples_x,
                _samples_y,
                marker="x",
                markeredgecolor="magenta",
                markersize=10,
                linestyle="none",
                linewidth=10,
            )

        ax.plot(
            self.evaluated_curve[0],
            self.evaluated_curve[1],
            color="navy",
            linestyle="solid",
            linewidth=3,
        )

        if _knots_shown:
            for i, knot_num in enumerate(self.KV):
                # plot only the first knot of any repeated knot
                if i == 0:
                    # print(f"first index {i}")
                    if self.LATEX:
                        _str = r"$\mathsf T_{0}$"
                    else:
                        _str = r"$T_{0}$"
                    k = i  # first evaluated knot index
                else:
                    if self.KV[i] == self.KV[i - 1]:
                        continue  # don't plot subsequently repeated knots

                    # print(f"subsequent index {i}")
                    # _Ti = str(int(i + self.DEGREE))
                    _Ti = str(int(i))
                    if self.LATEX:
                        _str = r"$\mathsf T_{" + _Ti + "}$"
                    else:
                        _str = r"$T_{" + _Ti + "}$"
                    k += 1  # next non-repeated knot index in evaluated knots

                # print(_str)
                ax.plot(
                    _evaluated_knots[0][k],
                    _evaluated_knots[1][k],
                    color="white",
                    alpha=0.6,
                    marker="o",
                    markersize=14,
                    markeredgecolor="darkcyan",
                )  # background circle
                ax.plot(
                    _evaluated_knots[0][k],
                    _evaluated_knots[1][k],
                    color="black",
                    marker=_str,
                    markersize=9,
                    markeredgecolor="none",
                )  # knot number text

        # self.fig.patch.set_facecolor("whitesmoke")
        # ax.set_facecolor("lightgray")

        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")

        # finish figure by calling method with common figure functions
        ViewBSplineFigure(self)


# class ViewBSplineSurface(ViewBSplineBase):
# TODO

# class ViewBSplineVolume(ViewBSplineBase):
# TODO


class ViewBSplineCurveFit(ViewBSplineFitBase):
    """Creates a Matplotlib figure of BSpline curve fitted to sample points."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SAMPLES = kwargs.get("samples", None)
        assert self.SAMPLES is not None

        _sample_time_method = kwargs.get("sample_time_method", "chord")

        # _BFit = bspfit.BSplineFit(self.SAMPLES, self.DEGREE, self.VERBOSITY, **kwargs)
        _fit = bspfit.BSplineFit(
            self.SAMPLES, self.DEGREE, self.VERBOSITY, _sample_time_method
        )

        # only "class", "degree", and "name" required by ViewBSplineFactory, so
        # manually propigate all other keys and values, with "class" overwrite.
        kwargs["class"] = "curve"  # replace "curvefit" with "curve" now to make curve
        kwargs["coefficients"] = _fit.control_points
        # kwargs["display"] = self.DISPLAY
        # kwargs["dpi"] = self.DPI
        kwargs["knot_vector"] = _fit.knot_vector
        # kwargs["latex"] = self.LS
        # kwargs["nbi"] = self.NBI
        kwargs["ncp"] = _fit.n_control_points
        # kwargs["serialize"] = self.SERIALIZE
        # kwargs["verbosity"] = self.VERBOSITY
        # kwargs["xticks"] = self.XTICKS
        # kwargs["yticks"] = self.YTICKS

        _vbsplinecurve = ViewBSplineCurve(**kwargs)


class ViewBSplineFigure:
    # def __init__(self, ViewBSplineBase):
    def __init__(self, base: ViewBSplineBase):
        # base = ViewBSplineBase
        ax = base.fig.gca()
        ax.set_aspect("equal")
        # ax.grid(True, which="major", linestyle="-", color="whitesmoke")
        ax.grid(True, which="major", linestyle="-")
        ax.grid(True, which="minor", linestyle=":")
        # ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

        if base.XTICKS:
            ax.set_xticks(base.XTICKS)

        if base.YTICKS:
            ax.set_yticks(base.YTICKS)

        if base.DISPLAY:
            # plt.show()
            plt.show(block=False)

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


def main(argv):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "config_file",
        help=".json BSpline basis, curve, curvefit, surface, volume specification",
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
    return item


if __name__ == "__main__":
    main(sys.argv[1:])
