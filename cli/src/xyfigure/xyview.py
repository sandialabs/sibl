# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports
import os
from datetime import datetime

# related third-party imports
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

# local application/library specific imports
# from xyfigure.xybase import XYBase
# from xyfigure.code.xybase import XYBase
from xyfigure.xybase import XYBase


class XYViewBase(XYBase):
    """The base class used by all XYViews."""

    def __init__(self, guid, **kwargs):
        super().__init__(guid, **kwargs)
        self._models = []
        self._model_keys = kwargs.get("model_keys", None)
        self._figure = None
        # self._folder = kwargs.get('folder', None)
        self._file_base = self._file.split(".")[0]

        self._title = kwargs.get("title", "default title")
        self._xlabel = kwargs.get("xlabel", "default x axis label")
        self._ylabel = kwargs.get("ylabel", "default y axis label")

        self._xticks = kwargs.get("xticks", None)
        self._yticks = kwargs.get("yticks", None)

        self._size = kwargs.get("size", [11.0, 8.5])
        self._dpi = kwargs.get("dpi", 100)
        self._xlim = kwargs.get("xlim", None)
        self._ylim = kwargs.get("ylim", None)

        self._display = kwargs.get("display", True)
        self._details = kwargs.get("details", True)
        # self._serialize = kwargs.get('serialize', False) # moved up to XYBase
        self._latex = kwargs.get("latex", False)
        if self._latex:
            from matplotlib import rc

            rc("text", usetex=True)
            rc("font", family="serif")

        # default value if axes_kwargs not client-supplied
        # https://matplotlib.org/stable/api/axes_api.html
        # https://matplotlib.org/stable/api/axes_api.html#appearance
        # whether frame (rectangle outline) appears on all axes
        self._frame = kwargs.get("frame", True)

        # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/axes_props.html#sphx-glr-gallery-subplots-axes-and-figures-axes-props-py
        #
        # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.tick_params.html#matplotlib.axes.Axes.tick_params
        # default to empty dictionary
        self._tick_params = kwargs.get("tick_params", {})

        print("Finished XYViewBase constructor.")

    @property
    def models(self):
        return self._models

    @models.setter
    def models(self, value):
        self._models = value

    @property
    def model_keys(self):
        return self._model_keys

    def figure(self):
        pass

    def serialize(self, folder, filename):  # extend base class
        # deprecated
        # super().serialize(folder, filename)
        # self._figure.savefig(
        #     self._path_file_output, dpi=self._dpi, bbox_inches="tight"
        # )  # avoid cutoff of labels
        # print(f"  Serialized view to: {self._path_file_output}")

        # New for XYView class, the so-called input file (input by the user) is the
        # output file to which the figure should be serialized.
        self._figure.savefig(
            self._path_file_input, dpi=self._dpi, bbox_inches="tight"
        )  # avoid cutoff of labels
        print(f"  Serialized view to: {self._path_file_input}")


class XYView(XYViewBase):
    """Creates a view that sees models."""

    def __init__(self, guid, **kwargs):
        super().__init__(guid, **kwargs)
        # self._models = []
        # self._model_keys = kwargs.get("model_keys", None)
        # self._figure = None
        # # self._folder = kwargs.get('folder', None)
        # self._file_base = self._file.split(".")[0]

        # default value if figure_kwargs not client-supplied
        # self._title = kwargs.get("title", "default title")
        # self._xlabel = kwargs.get("xlabel", "default x axis label")
        # self._ylabel = kwargs.get("ylabel", "default y axis label")

        # self._xticks = kwargs.get("xticks", None)
        # self._yticks = kwargs.get("yticks", None)

        self._xaxislog = kwargs.get("xaxis_log", False)
        self._yaxislog = kwargs.get("yaxis_log", False)

        # default = {'scale': 1, 'label': 'ylabel_rhs', 'verification': 0}
        self._yaxis_rhs = kwargs.get("yaxis_rhs", None)

        # inches, U.S. paper, landscape
        # self._size = kwargs.get("size", [11.0, 8.5])
        # self._dpi = kwargs.get("dpi", 100)
        # self._xlim = kwargs.get("xlim", None)
        # self._ylim = kwargs.get("ylim", None)

        self._background_image = kwargs.get("background_image", None)

        # self._display = kwargs.get("display", True)
        # self._details = kwargs.get("details", True)
        # # self._serialize = kwargs.get('serialize', False) # moved up to XYBase
        # self._latex = kwargs.get("latex", False)
        # if self._latex:
        #     from matplotlib import rc

        #     rc("text", usetex=True)
        #     rc("font", family="serif")

    # @property
    # def models(self):
    #     return self._models

    # @models.setter
    # def models(self, value):
    #     self._models = value

    # @property
    # def model_keys(self):
    #     return self._model_keys

    def figure(self):
        """Create a figure (view) of the registered models to the screen."""
        if self._figure is None:

            # dpi versus fig size
            # https://stackoverflow.com/questions/47633546/relationship-between-dpi-and-figure-size
            # fig, ax = plt.subplots(nrows=1, dpi=self._dpi)
            self._figure, ax = plt.subplots(nrows=1, dpi=self._dpi)
            if self._verbose:
                print(f"  Figure dpi set to {self._dpi}")

            # ax.ticklabel_format(axis='y', style='scientific')
            # ax.ticklabel_format(axis='both', style='scientific', scilimits=(0,0))

            # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.set_size_inches
            # fig.set_size_inches(self._size)
            self._figure.set_size_inches(self._size)
            if self._verbose:
                print("  Figure size set to " + str(self._size) + " inches.")

            if self._background_image:
                folder = self._background_image.get("folder", ".")
                file = self._background_image.get("file", None)
                # rel_path_and_file = os.path.join(
                #     folder, file
                # )  # relative to current run location
                path_file = Path(folder).expanduser().joinpath(file)
                # im = Image.open(rel_path_and_file)
                im = Image.open(path_file)

                left = self._background_image.get("left", 0.0)
                right = self._background_image.get("right", 1.0)
                bottom = self._background_image.get("bottom", 0.0)
                top = self._background_image.get("top", 1.0)
                al = self._background_image.get("alpha", 1.0)

                # https://github.com/matplotlib/matplotlib/issues/3173
                # https://matplotlib.org/3.1.1/tutorials/intermediate/imshow_extent.html
                bounds = [left, right, bottom, top]
                im = ax.imshow(im, zorder=0, extent=bounds, alpha=al, aspect="auto")

            for model in self._models:
                # needs rearchitecting, a logview descends from a view
                if self._xaxislog and not self._yaxislog:  # needs rearchitecting
                    ax.semilogx(model.x, model.y, **model.plot_kwargs)
                elif not self._xaxislog and self._yaxislog:
                    ax.semilogy(model.x, model.y, **model.plot_kwargs)
                elif self._xaxislog and self._yaxislog:
                    ax.loglog(model.x, model.y, **model.plot_kwargs)
                else:
                    ax.plot(model.x, model.y, **model.plot_kwargs)

            if self._xticks:
                ax.set_xticks(self._xticks)

            if self._yticks:
                ax.set_yticks(self._yticks)

            if self._xlim:
                ax.set_xlim(self._xlim)

            if self._ylim:
                ax.set_ylim(self._ylim)

            if self._yaxis_rhs:
                rhs_axis_scale = self._yaxis_rhs.get("scale", 1)
                rhs_axis_label = self._yaxis_rhs.get("label", None)
                # rhs_yticks_str = self._yaxis_rhs.get('yticks', None)
                rhs_yticks = self._yaxis_rhs.get("yticks", None)

                # ax2 = fig.add_subplot(111, sharex=ax, frameon=False)
                ax2 = self._figure.add_subplot(111, sharex=ax, frameon=False)
                bottom, top = ax.get_ylim()  # get from left-hand-side y-axis
                ax2.set_ylim(rhs_axis_scale * bottom, rhs_axis_scale * top)
                ax2.yaxis.tick_right()
                # ax2.ticklabel_format(axis='both', style='scientific', scilimits=(0,0))
                # ax.ticklabel_format(axis='both', style='scientific', scilimits=(0,0))
                # _ticklabel_format = self._yaxis_rhs.get('ticklabel_format', None)
                # _ticklabel_format = self._yaxis_rhs.get('ticklabel_format', None)
                # if _ticklabel_format:
                #     scilimits_str = _ticklabel_format.get('scilimitsl', "(0, 0)")
                #     ax2.ticklabel_format(**_ticklabel_format)
                # ax2.ticklabel_format(axis='both', style='scientific', scilimits=(0,0))
                # plt.ticklabel_format(axis='y', style='scientific', useOffset=False)
                # ax2.ticklabel_format(axis='y', style='scientific', useOffset=False)
                if rhs_yticks:
                    ax2.set_yticks(rhs_yticks)
                ax2.yaxis.set_label_position("right")
                ax2.set_ylabel(rhs_axis_label)

            # fig.suptitle(self._title)
            self._figure.suptitle(self._title)
            ax.set_xlabel(self._xlabel)
            ax.set_ylabel(self._ylabel)
            # set frame on or off based on the Bool "frame" in .json input
            ax.set_frame_on(b=self._frame)
            if len(self._tick_params) > 0:
                ax.tick_params(**self._tick_params)
            ax.grid()
            ax.legend()

            if self._details:
                now = datetime.now()
                now_str = now.strftime("%Y-%m-%d %H:%M:%S")
                user = str(os.getlogin())
                host = str(os.getenv("HOSTNAME"))
                details_str = (
                    self._file + " created " + now_str + " by " + user + " on " + host
                )
                ax.set_title(details_str, fontsize=10, ha="center", color="dimgray")

            if self._display:
                plt.show()

            if self._serialize:
                self.serialize(self._folder, self._file)

            plt.close("all")
            self._figure = None

    # def serialize(self, folder, filename):  # extend base class
    #     # deprecated
    #     # super().serialize(folder, filename)
    #     # self._figure.savefig(
    #     #     self._path_file_output, dpi=self._dpi, bbox_inches="tight"
    #     # )  # avoid cutoff of labels
    #     # print(f"  Serialized view to: {self._path_file_output}")

    #     # New for XYView class, the so-called input file (input by the user) is the
    #     # output file to which the figure should be serialized.
    #     self._figure.savefig(
    #         self._path_file_input, dpi=self._dpi, bbox_inches="tight"
    #     )  # avoid cutoff of labels
    #     print(f"  Serialized view to: {self._path_file_input}")


class XYViewAbaqus(XYViewBase):
    """Creates an ABAQUS view that sees ABAQUS models."""

    def __init__(self, guid, **kwargs):
        super().__init__(guid, **kwargs)
        # self._models = []
        # self._model_keys = kwargs.get("model_keys", None)
        # self._figure = None
        # # self._folder = kwargs.get('folder', None)
        # self._file_base = self._file.split(".")[0]

        # default value if figure_kwargs not client-supplied
        # self._title = kwargs.get("title", "default title")
        # self._xlabel = kwargs.get("xlabel", "default x axis label")
        # self._ylabel = kwargs.get("ylabel", "default y axis label")

        # self._xticks = kwargs.get("xticks", None)
        # self._yticks = kwargs.get("yticks", None)

        # inches, U.S. paper, landscape
        # self._size = kwargs.get("size", [11.0, 8.5])
        # self._dpi = kwargs.get("dpi", 100)
        # self._xlim = kwargs.get("xlim", None)
        # self._ylim = kwargs.get("ylim", None)

        # self._display = kwargs.get("display", True)
        # self._details = kwargs.get("details", True)
        # # self._serialize = kwargs.get('serialize', False) # moved up to XYBase
        # self._latex = kwargs.get("latex", False)
        # if self._latex:
        #     from matplotlib import rc

        #     rc("text", usetex=True)
        #     rc("font", family="serif")

    @property
    def models(self):
        return self._models

    @models.setter
    def models(self, value):
        self._models = value

    @property
    def model_keys(self):
        return self._model_keys

    def figure(self):
        """Create a figure (view) of the registered models to the screen."""
        if self._figure is None:

            self._figure, ax = plt.subplots(nrows=1, dpi=self._dpi)
            if self._verbose:
                print(f"  Figure dpi set to {self._dpi}")

            self._figure.set_size_inches(self._size)
            if self._verbose:
                print("  Figure size set to " + str(self._size) + " inches.")

            for model in self._models:
                xs, ys, _ = zip(*model._nodes)

                for face in model._elements:
                    xf = tuple(xs[k - 1] for k in face)  # 1-base index to 0-base index
                    yf = tuple(ys[k - 1] for k in face)
                    # plt.fill(
                    #     xf,
                    #     yf,
                    #     linestyle="dotted",
                    #     edgecolor="magenta",
                    #     alpha=0.5,
                    #     facecolor="gray",
                    # )
                    plt.fill(
                        xf,
                        yf,
                        alpha=model._alpha,
                        edgecolor=model._edgecolor,
                        facecolor=model._facecolor,
                        linestyle=model._linestyle,
                        linewidth=model._linewidth,
                    )

            if self._xticks:
                ax.set_xticks(self._xticks)

            if self._yticks:
                ax.set_yticks(self._yticks)

            if self._xlim:
                ax.set_xlim(self._xlim)

            if self._ylim:
                ax.set_ylim(self._ylim)

            if self._xlabel:
                ax.set_xlabel(self._xlabel)

            if self._ylabel:
                ax.set_ylabel(self._ylabel)

            # set frame on or off based on the Bool "frame" in .json input
            ax.set_frame_on(b=self._frame)
            if len(self._tick_params) > 0:
                ax.tick_params(**self._tick_params)

            if self._display:
                plt.show()

            if self._serialize:
                self.serialize(self._folder, self._file)

            plt.close("all")
            self._figure = None


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
