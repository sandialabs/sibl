# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


from abc import ABC
import argparse
import json
from pathlib import Path
import sys
from typing import List

# from matplotlib.ticker import AutoMinorLocator
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import MultipleLocator
import matplotlib.tri as mtri
import numpy as np

import ptg.bspline as bsp
import ptg.bspline_fit as bspfit

"""
$ conda active siblenv
$ cd ~/sibl/geo/src/ptg
$ python view_bspline.py model_config.json
e.g.
$ python view_bspline.py ../../data/bspline/recover_bezier_linear.json
$ python view_bspline.py ../../data/bspline/recover_bezier_linear.json --verbose
"""

colors = ("tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:cyan")

defaults = {
    "control_net_kwargs": {
        "alpha": 0.5,
        "color": "red",
        "linestyle": "dashed",
        "linewidth": 1,
    },
    "control_points_kwargs": {
        "alpha": 0.5,
        "color": "red",
        "linestyle": "None",
        "linewidth": 1,
        "marker": "o",
        "markerfacecolor": "white",
        "markersize": 9,
    },
    "evaluation_points_kwargs": {
        "alpha": 0.5,
        "color": "navy",
        "linestyle": "None",
        "linewidth": 0.5,
        "marker": ".",
        "markersize": 4,
        "markeredgecolor": "None",
        "markerfacecolor": "navy",
    },
    "surface_kwargs": {"alpha": 0.6, "edgecolor": "lightgray", "linewidth": 0.125},
}


class ControlNet:
    """Creates a control net for a BSpline surface.

    Arguments:
        control_points (List[List[List[float]]]): the control points arranged
            in `t` direction rows, `u` direction columns, and `(x, y, z)` values
    """

    def __init__(self, control_points: List[List[List[float]]]) -> None:
        self._rows = np.array(control_points)
        (self.n_rows, self.n_cols, self.nsd) = self._rows.shape
        self._cols = [self._rows[:, j, :] for j in np.arange(self.n_cols)]

    @property
    def rows(self):
        """Returns a numpy array of `(x, y, z)` points composing each row."""
        return self._rows

    @property
    def columns(self):
        """Returns a numpy array of `(x, y, z)` points composing each column."""
        return self._cols


class ViewBSplineFactory:
    """The one and only (singleton) factory for ViewBSpline objects."""

    @staticmethod
    def create(config: str, verbose: bool = True):
        """Creates a ViewBSpline object that is listed in ViewBSplineFactory.

        Args:
            config (str): the .json file name, with path, that specifies dictionary of
                keys and values used to construct ViewBSpline objects.
            verbose (Optional[bool]): True provides feedback during run, False does not.
                Defaults to True.

        Returns:
            A ViewBSplineInstance identified in the factory by the config file.
        """

        if not Path(config).is_file():
            sys.exit(f"Error: cannot find file {config}")

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
        #     "degree_t",
        #     "name",
        #     "ncp",
        # )
        _config_schema = ("class", "degree_t", "name")

        # check .json input schema
        for item in _config_schema:
            value = kwargs.get(item, None)
            if not value:
                sys.exit(f'Error: keyword "{item}" not found in config input file.')

        _factory_items = {
            "basis": ViewBSplineBasis,
            "curve": ViewBSplineCurve,
            "curvefit": ViewBSplineCurveFit,
            "surface": ViewBSplineSurface,
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
        # keep attributes in alphabetical order here:
        self.camera_elevation = kwargs.get("camera-elevation", None)
        self.camera_azimuth = kwargs.get("camera-azimuth", None)

        # The control net connects the control points in an array, net, or lattice.
        self.control_net_alpha = kwargs.get("control_net_alpha", 0.5)
        self.control_net_color = kwargs.get("control_net_color", "red")
        self.control_net_linestyle = kwargs.get("control_net_linestyle", "dashed")
        self.control_net_linewidth = kwargs.get("control_net_linewidth", 1)
        self.control_net_shown = kwargs.get("control_net_shown", True)

        # The control points are the discrete (x,y) or (x,y,z) points in space.
        self.control_points_alpha = kwargs.get("control_points_alpha", 0.5)
        self.control_points_color = kwargs.get("control_points_color", "red")
        self.control_points_linestyle = kwargs.get("control_points_linestyle", "dashed")
        self.control_points_linewidth = kwargs.get("control_points_linewidth", 1)
        self.control_points_marker = kwargs.get("control_points_marker", "o")
        self.control_points_marker_facecolor = kwargs.get(
            "control_points_marker_facecolor", "white"
        )
        self.control_points_marker_size = kwargs.get("control_points_marker_size", 9)
        self.control_points_shown = kwargs.get("control_points_shown", True)

        # factory has already checked items are specified, no default values necessary
        # 0 constant, 1 linear, 2 quadratic, etc.
        self.degree_t = kwargs.get("degree_t")
        self.degree_u = kwargs.get("degree_u", None)

        # get config specification, specify defaults otherwise
        self.display = kwargs.get("display", False)  # True shows figure to screen
        self.dpi = kwargs.get("dpi", 100)  # dots per inch

        # show evaulation points for parameters t, u, and v
        self.evaluation_points_alpha = kwargs.get("evaluation_points_alpha", 0.5)
        self.evaluation_points_color = kwargs.get("evaluation_points_color", "navy")
        self.evaluation_points_linestyle = kwargs.get(
            "evaluation_points_linestyle", "solid"
        )
        self.evaluation_points_linewidth = kwargs.get("evaluation_points_linewidth", 1)
        self.evaluation_points_marker = kwargs.get("control_points_marker", ".")
        # self.evaluation_points_marker_facecolor = kwargs.get(
        #     "evluation_points_marker_facecolor", "white"
        # )
        self.evaluation_points_marker_size = kwargs.get(
            "evaluation_points_marker_size", 1
        )
        self.evaluation_points_shown = kwargs.get("evaluation_points_shown", False)

        self.latex = kwargs.get("latex", False)  # use LaTeX instead of default fonts
        if self.latex:
            rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
            rc("text", usetex=True)
        self.linestyles = kwargs.get(
            "linestyles", ("solid", "dashed", "dashdot")
        )  # linestyles

        self.name = kwargs.get("name")  # name is used for output file name
        self.nbi = kwargs.get("nbi", 2)  # number of bisections per knot interval
        self.plot3d = False  # False is 2D, descendants overwrite to True for 3D

        self.serialize = kwargs.get("serialize", False)  # save figure to disc
        self.surface_triangulation = kwargs.get(
            "surface_triangulation", False
        )  # surface
        self.surface_triangulation_alpha = kwargs.get(
            "surface_triangulation_alpha", 1.0
        )  # surface or volume

        # https://matplotlib.org/3.1.0/users/dflt_style_changes.html
        # color C0 is same as "#1f77b4", a medium-dark cyan
        self.surface_triangulation_color = kwargs.get(
            "surface_triangulation_color", "C0"
        )
        self.xlim = kwargs.get("xlim", None)
        self.ylim = kwargs.get("ylim", None)
        self.zlim = kwargs.get("zlim", None)

        self.xticks = kwargs.get("xticks", None)
        self.yticks = kwargs.get("yticks", None)
        self.zticks = kwargs.get("zticks", None)
        self.z_axis_label_inverted = kwargs.get("z-axis-label-inverted", True)

        self.verbosity = kwargs.get("verbosity", False)


class ViewBSplineBase(ViewBase):
    """Base class for ViewBSplineCurveFit class."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.NCP = kwargs.get("ncp")

        _KNOT_OFFSET = kwargs.get(
            "knot_offset", 0
        )  # translate knot vector to left or right

        _a, _b = 0, self.NCP - self.degree_t
        _knot_vector_default = (
            np.concatenate(
                (
                    np.repeat(_a, self.degree_t),
                    np.arange(_a, _b),
                    np.repeat(_b, self.degree_t + 1),
                )
            )
            + _KNOT_OFFSET
        )
        # default is open knot vector, no internal knot multiplicity
        self.knot_vector_t = kwargs.get("knot_vector_t", None)

        if self.knot_vector_t is None:
            self.knot_vector_t = _knot_vector_default
            print("Warning: 'knot_vector_t' key not found, using default knot")
            print("  vector, assumes no internal knot multiplicity.")

        # number of elements is the number of non-zero knot spans
        self.nel = len(np.unique(self.knot_vector_t)) - 1

        print(f"Computing B-spline basis with degree = {self.degree_t}")
        print(f"  with knot vector {self.knot_vector_t}")
        print(f"  of {len(self.knot_vector_t)} knots")
        print(f"  with number of bisections per knot interval = {self.nbi}")
        print(f"  with number of elements (non-zero knot spans) = {self.nel}")

        _knots_lhs = self.knot_vector_t[0:-1]  # left-hand-side knot values
        _knots_rhs = self.knot_vector_t[1:]  # right-hand-side knot values
        _knot_spans = np.array(_knots_rhs) - np.array(_knots_lhs)
        _dt = _knot_spans / (2**self.nbi)
        assert all([dti >= 0 for dti in _dt]), "Error: knot vector is decreasing."

        _num_knots = len(self.knot_vector_t)
        _t = [
            _knots_lhs[k] + j * _dt[k]
            for k in np.arange(_num_knots - 1)
            for j in np.arange(2**self.nbi)
        ]
        _t.append(self.knot_vector_t[-1])  # evauation times
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

            _B = bsp.Curve(self.knot_vector_t, coef, self.degree_t)

            if _B.is_valid():
                _y = _B.evaluate(self.evaluation_times)
                self.evaluated_bases.append(_y)

        # plot B-spline basis functions
        self.fig = plt.figure(figsize=plt.figaspect(1.0 / (self.nel + 1)), dpi=self.dpi)
        ax = self.fig.gca()

        # loop over each basis function and plot it
        for i in np.arange(self.NCP):
            _CPTXT = f"{i}"
            _DEGTXT = f"{self.degree_t}"
            ax.plot(
                self.evaluation_times,
                self.evaluated_bases[i],
                lw=2,
                label="$N_{" + _CPTXT + "}^{" + _DEGTXT + "}$",
                linestyle=self.linestyles[np.remainder(i, len(self.linestyles))],
            )

        ax.set_xlabel(r"$t$")
        ax.set_ylabel(f"$N^{self.degree_t}_i(t)$")

        _eps = 0.1
        ax.set_xlim(
            [self.knot_vector_t[0] - 2 * _eps, self.knot_vector_t[-1] + 2 * _eps]
        )
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
            _knots_t = np.unique(self.knot_vector_t)

        # show/hide sample points in case of a B-spline fit
        _samples_shown = kwargs.get("samples_shown", False)

        # build up B-spline basis functions, multiplied by coefficients
        _NSD = len(COEF[0])  # number of space dimensions
        assert _NSD == 2  # only 2D curves implemented for now, do 3D later

        for i in np.arange(_NSD):

            coef = np.array(COEF)[:, i]

            _B = bsp.Curve(self.knot_vector_t, coef, self.degree_t)

            if _B.is_valid():
                _y = _B.evaluate(self.evaluation_times)
                self.evaluated_curve.append(_y)

                if _knots_shown:
                    _y = _B.evaluate(_knots_t)
                    _evaluated_knots.append(_y)

        # plot B-spline curve, assume 2D for now
        self.fig = plt.figure(dpi=self.dpi)
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
                color="darkorange",
                alpha=1.0,
                linestyle="none",
                linewidth="6",
                marker="+",
                markersize=20,
            )  # plus mark
            ax.plot(
                _samples_x,
                _samples_y,
                color="orange",
                linestyle="none",
                marker="D",
                markerfacecolor="none",
                markersize=14,
            )  # diamond border around plus mark

        ax.plot(
            self.evaluated_curve[0],
            self.evaluated_curve[1],
            color="navy",
            linestyle="solid",
            linewidth=3,
        )

        if _samples_shown:  # yet another layer for samples, small little dot atop curve
            _samples_x = np.array(kwargs.get("samples"))[:, 0]
            _samples_y = np.array(kwargs.get("samples"))[:, 1]
            ax.plot(
                _samples_x,
                _samples_y,
                color="darkorange",
                linestyle="none",
                marker=".",
                markersize=2,
            )  # dot

        if _knots_shown:
            for i, knot_num in enumerate(self.knot_vector_t):
                # plot only the first knot of any repeated knot
                if i == 0:
                    # print(f"first index {i}")
                    k = i  # first evaluated knot index
                    if self.latex:
                        _str = r"$\mathsf T_{0}$"
                    else:
                        # _str = r"$T_{0}$"
                        continue  # GitHub unit test doesn't like LaTex
                else:
                    if self.knot_vector_t[i] == self.knot_vector_t[i - 1]:
                        continue  # don't plot subsequently repeated knots

                    # print(f"subsequent index {i}")
                    k += 1  # next non-repeated knot index in evaluated knots

                    # _Ti = str(int(i + self.degree_t))
                    _Ti = str(int(i))
                    if self.latex:
                        _str = r"$\mathsf T_{" + _Ti + "}$"
                    else:
                        # _str = r"$T_{" + _Ti + "}$"
                        continue  # GitHub unit test doesn't like LaTex

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


class ViewBSplineSurface(ViewBase):
    """Creates a Matplotlib figure of BSpline surface."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plot3d = True  # overwrite the base class
        COEF = kwargs.get(
            "coefficients", None
        )  # None is basis, not None is curve, surface, or volume
        assert COEF is not None

        _NSD = len(COEF[0][0])  # number of space dimensions
        assert _NSD == 3  # only 2D curves implemented for now, do 3D later

        # plot B-spline curve, assume 2D for now
        self.fig = plt.figure(dpi=self.dpi)
        # ax = self.fig.gca()
        ax = self.fig.add_subplot(111, projection="3d")

        # avoid "magic" numbers, assign (0, 1, 2) to variables
        idx, idy, idz = (0, 1, 2)

        # self.control_net_alpha = kwargs.get("control_net_alpha", 0.5)
        # self.control_net_color = kwargs.get("control_net_color", "magenta")
        # self.control_net_linestyle = kwargs.get("control_net_linestyle", "dashed")
        # self.control_net_linewidth = kwargs.get("control_net_linewidth", 1)
        # self.control_net_shown = kwargs.get("control_net_shown", True)

        if self.control_net_shown:
            # create control net object
            cn = ControlNet(COEF)

            # draw control net rows
            _row_points = cn.rows
            for r in _row_points:
                ax.plot3D(
                    r[:, idx],
                    r[:, idy],
                    r[:, idz],
                    alpha=self.control_net_alpha,
                    color=self.control_net_color,
                    linestyle=self.control_net_linestyle,
                    linewidth=self.control_net_linewidth,
                )

            # draw control net columns
            _col_points = cn.columns
            for c in _col_points:
                ax.plot3D(
                    c[:, idx],
                    c[:, idy],
                    c[:, idz],
                    alpha=self.control_net_alpha,
                    color=self.control_net_color,
                    linestyle=self.control_net_linestyle,
                    linewidth=self.control_net_linewidth,
                )

        if self.control_points_shown:

            # plot control points
            _cp_x = np.array(COEF)[:, :, idx].flatten()  # control points x-coordinates
            _cp_y = np.array(COEF)[:, :, idy].flatten()  # control points y-coordinates
            _cp_z = np.array(COEF)[:, :, idz].flatten()  # control points z-coordinates

            ax.plot3D(
                _cp_x,
                _cp_y,
                _cp_z,
                alpha=self.control_points_alpha,
                color=self.control_points_color,
                linestyle=self.control_points_linestyle,
                linewidth=self.control_points_linewidth,
                marker=self.control_points_marker,
                markerfacecolor=self.control_points_marker_facecolor,
                markersize=self.control_points_marker_size,
            )

        if self.evaluation_points_shown or self.surface_triangulation:

            kv_t = kwargs.get("knot_vector_t")
            kv_u = kwargs.get("knot_vector_u")
            # control_poiknts argument already exists as COEF variable

            # S = bsp.Surface(
            #     kv_t, kv_u, COEF, self.degree_t, self.degree_u, verbose=self.verbosity
            # )
            S = bsp.Surface(
                knot_vector_t=kv_t,
                knot_vector_u=kv_u,
                coefficients=COEF,
                degree_t=self.degree_t,
                degree_u=self.degree_u,
                n_bisections=self.nbi,
                verbose=self.verbosity,
            )

            (_surf_x, _surf_y, _surf_z) = S.evaluations

            if self.evaluation_points_shown:
                ax.plot3D(
                    _surf_x.flatten(),
                    _surf_y.flatten(),
                    _surf_z.flatten(),
                    alpha=self.evaluation_points_alpha,
                    color=self.evaluation_points_color,
                    linestyle=self.evaluation_points_linestyle,
                    linewidth=self.evaluation_points_linewidth,
                    marker=self.evaluation_points_marker,
                    markersize=self.evaluation_points_marker_size,
                )
                # markerfacecolor=self.evaluation_points_marker_facecolor,

            if self.surface_triangulation:
                # convention here is reverse of the (x, y) convention of
                # mesh grid, see
                # https://numpy.org/doc/stable/reference/generated/numpy.meshgrid.html
                u, t = np.meshgrid(S.evaluation_times_u, S.evaluation_times_t)
                u, t = u.flatten(), t.flatten()

                tri = mtri.Triangulation(u, t)
                ax.plot_trisurf(
                    _surf_x.flatten(),
                    _surf_y.flatten(),
                    _surf_z.flatten(),
                    alpha=self.surface_triangulation_alpha,
                    triangles=tri.triangles,
                )

                # color=self.surface_triangulation_color,

        xlabel = kwargs.get("xlabel", "x")
        ylabel = kwargs.get("ylabel", "y")
        zlabel = kwargs.get("zlabel", "z")

        # ax.set_xlabel(r"$x$")
        # ax.set_ylabel(r"$y$")

        ax.set_xlabel(r"" + xlabel + "")
        ax.set_ylabel(r"" + ylabel + "")
        ax.set_zlabel(r"" + zlabel + "")

        if self.xlim:
            ax.set_xlim(self.xlim)

        if self.ylim:
            ax.set_ylim(self.ylim)

        if self.zlim:
            ax.set_zlim(self.zlim)

        # finish figure by calling method with common figure functions
        ViewBSplineFigure(self)


# class ViewBSplineVolume(ViewBSplineBase):
# TODO


class ViewBSplineCurveFit(ViewBSplineFitBase):
    """Creates a Matplotlib figure of BSpline curve fitted to sample points."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SAMPLES = kwargs.get("samples", None)
        assert self.SAMPLES is not None

        _sample_time_method = kwargs.get("sample_time_method", "chord")

        # _BFit = bspfit.BSplineFit(self.SAMPLES, self.degree_t, self.verbosity, **kwargs)
        _fit = bspfit.BSplineFit(
            self.SAMPLES, self.degree_t, self.verbosity, _sample_time_method
        )

        # only "class", "degree_t", and "name" required by ViewBSplineFactory, so
        # manually propigate all other keys and values, with "class" overwrite.
        kwargs["class"] = "curve"  # replace "curvefit" with "curve" now to make curve
        kwargs["coefficients"] = _fit.control_points
        # kwargs["display"] = self.display
        # kwargs["dpi"] = self.dpi
        kwargs["knot_vector_t"] = _fit.knot_vector
        # kwargs["latex"] = self.linestyles
        # kwargs["nbi"] = self.nbi

        kwargs["ncp"] = _fit.n_control_points
        # kwargs["serialize"] = self.serialize
        # kwargs["verbosity"] = self.verbosity
        # kwargs["xticks"] = self.xticks
        # kwargs["yticks"] = self.yticks

        # _vbsplinecurve = ViewBSplineCurve(**kwargs)
        _ = ViewBSplineCurve(**kwargs)


class ViewBSplineFigure:
    # def __init__(self, ViewBSplineBase):
    def __init__(self, base: ViewBSplineBase):
        # base = ViewBSplineBase
        ax = base.fig.gca()
        if not base.plot3d:
            # then we have a 2D plot
            ax.set_aspect("equal")
            # ax.grid(True, which="major", linestyle="-", color="whitesmoke")
            ax.grid(True, which="major", linestyle="-")
            ax.grid(True, which="minor", linestyle=":")
            # ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
        else:
            # then we have a 3D plot
            if base.z_axis_label_inverted:
                ax.zaxis.set_rotate_label(False)
                ax.zaxis.label.set_rotation(90)

            if base.zticks:
                ax.set_zticks(base.zticks)

            if base.camera_azimuth or base.camera_elevation is not None:
                ax.view_init(elev=base.camera_elevation, azim=base.camera_azimuth)

        if base.xticks:
            ax.set_xticks(base.xticks)

        if base.yticks:
            ax.set_yticks(base.yticks)

        if base.display:  # same as INTERACTIVE in view_bezier.py
            plt.show()
        else:
            plt.show(block=False)

        if base.serialize:
            extension = ".pdf"  # or '.svg'
            if base.name is None:
                filename = (
                    "N(p=" + str(base.degree_t) + ")_NCP=" + str(base.NCP) + extension
                )
            else:
                filename = base.name + extension
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
