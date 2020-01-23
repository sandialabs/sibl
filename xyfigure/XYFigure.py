#!/usr/bin/env python
# Client to create figures for Military Specification journal manuscript.
# To run from command line with Python3:
# [base_directory]: $ python XYFigure.py

import os
import sys
from abc import ABC
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
# import imageio
from PIL import Image

#from matplotlib import rc
#rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
#rc('text', usetex=True)

# Figure Service
## Abstract Base Class
class XYBase(ABC):
    """
    Base class to collect all data and methods common to XYBase descendants.
    """
    def __init__(self, **kwargs):
        self._folder = kwargs['folder']
        self._file = kwargs['file']


## Model
class XYModel(XYBase):
    """The data to be plotted in XY format."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._skip_rows = kwargs.get('skip_rows', 0)
        self._skip_rows_footer = kwargs.get('skip_rows_footer', 0)
        self._xcolumn = kwargs.get('xcolumn', 0)  # default to the first column
        self._ycolumn = kwargs.get('ycolumn', 1)  # default to the second column

        # self._data = np.genfromtxt(self._file, dtype='float', delimiter=',', skip_header=self._skip_rows)
        path_and_file = os.path.join(self._folder, self._file)
        #self._data = np.genfromtxt(path_and_file, dtype='float', delimiter=',', skip_header=self._skip_rows)
        self._data = np.genfromtxt(path_and_file, dtype='float', delimiter=',', skip_header=self._skip_rows, skip_footer=self._skip_rows_footer, usecols=(self._xcolumn, self._ycolumn))

        # default value if plot_kwargs not client-supplied
        default = {'linewidth': 2.0, 'linestyle': '-'}
        self._plot_kwargs = kwargs.get('plot_kwargs', default)

        # self._inverted = kwargs.get('inverted', False)  # deprecated
        self._xscale = kwargs.get('xscale', 1.0)
        self._yscale = kwargs.get('yscale', 1.0)
        self._xoffset = kwargs.get('xoffset', 0.0)
        self._yoffset = kwargs.get('yoffset', 0.0)

    @property
    def x(self):
        """Returns the model's x data."""
        return self._data[:, 0] * self._xscale + self._xoffset

    @property
    def y(self):
        """Returns the model's y data."""
        return self._data[:, 1] * self._yscale + self._yoffset

    @property
    def plot_kwargs(self):
        """Returns kwargs passed to matplotlib.pyplot.plot()."""
        return self._plot_kwargs

    #@property
    #def is_inverted(self):
    #    return self._inverted

## View
class XYView(XYBase):
    """Creates a view that sees models."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._models = []
        self._figure = None
        # self._folder = kwargs.get('folder', None)
        self._file_base = self._file.split('.')[0]

        # default value if figure_kwargs not client-supplied
        self._title = kwargs.get('title', 'default title')
        self._xlabel = kwargs.get('xlabel', 'default x axis label')
        self._ylabel = kwargs.get('ylabel', 'default y axis label')

        self._xticks_str = kwargs.get('xticks', None)
        self._yticks_str = kwargs.get('yticks', None)
        # self._yticks_rhs_str = kwargs.get('yticks_rhs', None)

        self._x_log_scale = kwargs.get('x_log_scale', None)

        # default = {'scale': 1, 'label': 'ylabel_rhs', 'verification': 0}
        self._yaxis_rhs = kwargs.get('yaxis_rhs', None)

        # default value if figure_kwargs not client-supplied
        # default = {'figsize': '(11.0, 8.5)'}  # inches, U.S. paper, landscape
        # self._figure_args = kwargs.get('figure_args', default)
        # self._size_str = kwargs.get('size', '(11.0, 8.5)')
        self._size = kwargs.get('size', [11.0, 8.5])
        #self._xlim_str = kwargs.get('xlim', None)
        #self._ylim_str = kwargs.get('ylim', None)
        self._xlim = kwargs.get('xlim', None)
        self._ylim = kwargs.get('ylim', None)

        self._background_image = kwargs.get('background_image', None)

        self._display = kwargs.get('display', True)
        self._details = kwargs.get('details', True)
        self._serialize = kwargs.get('serialize', False)
        self._latex = kwargs.get('latex', False)
        if self._latex:
            from matplotlib import rc
            #rc('font', **{'family': 'serif', 'serif': ['Computer Modern Roman']})
            rc('text', usetex=True)
            rc('font', family='serif')

    @property
    def models(self):
        return self._models

    @models.setter
    def models(self, value):
        self._models = value

    def figure(self):
        """Create a figure (view) of the registered models to the screen."""
        if self._figure is None:

            # fig, ax = plt.subplots(nrows=1, **self._figure_args)
            # fig, ax = plt.subplots(nrows=1)  # temporary
            # fig, ax = plt.subplots(nrows=1, figsize=figsize_tuple)
            fig, ax = plt.subplots(nrows=1)

            # ax.ticklabel_format(axis='y', style='scientific')
            # ax.ticklabel_format(axis='both', style='scientific', scilimits=(0,0))

            #figsize_tuple_str = self._figure_args.get('figsize', None)
            #if figsize_tuple_str:
            #    figsize_tuple = eval(figsize_tuple_str)
            #    fig.set_size_inches(figsize_tuple)
            # size_tuple = eval(self._size_str)
            # fig.set_size_inches(size_tuple)
            fig.set_size_inches(self._size)
            # print('Figure size set to ' +  str(size_tuple) + ' inches.')
            print('Figure size set to ' +  str(self._size) + ' inches.')

            #fig.set_size_inches(figsize_tuple)  # https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.figure.Figure.html#matplotlib.figure.Figure.set_size_inches
            # self._folder = kwargs.get('folder', None)

            if self._background_image:
                folder = self._background_image.get('folder', '.')
                file = self._background_image.get('file', None)
                path_and_file = os.path.join(folder, file)
                # im = imageio.imread(path_and_file)
                im = Image.open(path_and_file)

                left = self._background_image.get('left', 0.0)
                right = self._background_image.get('right', 1.0)
                bottom = self._background_image.get('bottom', 0.0)
                top = self._background_image.get('top', 1.0)
                al = self._background_image.get('alpha', 1.0)

                # https://github.com/matplotlib/matplotlib/issues/3173
                # https://matplotlib.org/3.1.1/tutorials/intermediate/imshow_extent.html
                bounds = [left, right, bottom ,top]
                im = ax.imshow(im, zorder=0, extent=bounds, alpha=al, aspect='auto')

            for model in self._models:
                # needs rearchitecting, a logview descends from a view
                if self._x_log_scale:  # needs rearchitecting
                    ax.semilogx(model.x, model.y, **model.plot_kwargs)
                else:
                    ax.plot(model.x, model.y, **model.plot_kwargs)

            if self._xticks_str:
                ticks = eval(self._xticks_str)
                # plt.xticks(ticks)
                ax.set_xticks(ticks)

            if self._yticks_str:
                ticks = eval(self._yticks_str)
                # plt.yticks(ticks)
                ax.set_yticks(ticks)

            # xlim_tuple_str = self._figure_args.get('xlim', None)
            # if xlim_tuple_str:
            #     ax.set_xlim(eval(xlim_tuple_str))

            # ylim_tuple_str = self._figure_args.get('ylim', None)
            # if ylim_tuple_str:
            #     ax.set_ylim(eval(ylim_tuple_str))

            # if self._xlim_str:
            #     ax.set_xlim(eval(self._xlim_str))

            # if self._ylim_str:
            #     ax.set_ylim(eval(self._ylim_str))

            if self._xlim:
                ax.set_xlim(self._xlim)

            if self._ylim:
                ax.set_ylim(self._ylim)

            if self._yaxis_rhs:
                rhs_axis_scale = self._yaxis_rhs.get('scale', 1)
                rhs_axis_label = self._yaxis_rhs.get('label', None)
                rhs_yticks_str = self._yaxis_rhs.get('yticks', None)

                ax2 = fig.add_subplot(111, sharex=ax, frameon=False)
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
                if rhs_yticks_str:
                    ticks = eval(rhs_yticks_str)
                    # ax2.yaxis.set_yticks(ticks)
                    ax2.set_yticks(ticks)
                    # plt.yticks(ticks)
                ax2.yaxis.set_label_position('right')
                ax2.set_ylabel(rhs_axis_label)

            fig.suptitle(self._title)
            ax.set_xlabel(self._xlabel)
            ax.set_ylabel(self._ylabel)
            ax.grid()
            ax.legend()

            if self._details:
                now = datetime.now()
                now_str = now.strftime("%Y-%m-%d %H:%M:%S")
                user = str(os.environ.get('USERNAME'))
                details_str = self._file + ' created ' + now_str + ' by ' + user
                ax.set_title(details_str, fontsize=10, ha='center', color='dimgray')

            if self._display:
                plt.show()
            if self._serialize:
                folder = self._folder
                abs_path = os.path.join(os.getcwd(), folder)
                if not os.path.isdir(abs_path):
                    print(f'Folder needed but not found: "{abs_path}"')
                    val = input('Create folder? [y]es or [n]o : ')
                    if val == 'y':
                        os.mkdir(folder)
                        print(f'Created folder: "{folder}"')
                    else:
                        print('Check accuracy of folders in database.')
                        print('Abnormal script termination.')
                        sys.exit('Folder misspecified.')

                fig.savefig(os.path.join(abs_path, self._file), dpi=300)
                print('Figure saved to folder: ' + abs_path)
                print(f'Figure filename: {self._file}')

        #return fig, ax  # return so clients to further embellish

## Figure Factory
FACTORY_ITEMS = {
    'model': XYModel,
    'view': XYView
}

class XYFactory:
    """The one and only (singleton) factory for XY items."""
    @staticmethod
    def create(item, **kwargs):
        "Main factory method, returns XY objects."
        instance = FACTORY_ITEMS.get(kwargs['class'], None)
        if instance:
            return instance(**kwargs)

        # If we get here, we did not return an instance, so warn.
        print(f'Warning: {item} requested but not provided by this factory, returning None.')
        return None
