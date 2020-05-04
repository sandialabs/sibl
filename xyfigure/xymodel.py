import os
import sys

# from importlib import import_module
# import importlib.util as ilu

import numpy as np
from scipy import signal
from scipy.integrate import cumtrapz

# from xybase import XYBase
from xyfigure.xybase import XYBase


class XYModel(XYBase):
    """The data to be plotted in XY format."""
    def __init__(self, guid, **kwargs):
        super().__init__(guid, **kwargs)

        self._skip_rows = kwargs.get('skip_rows', 0)
        self._skip_rows_footer = kwargs.get('skip_rows_footer', 0)
        self._xcolumn = kwargs.get('xcolumn', 0)  # default to the first column
        self._ycolumn = kwargs.get('ycolumn', 1)  # default to the second column

        rel_path_and_file = os.path.join(self._folder, self._file)  # relative to current run location
        self._data = np.genfromtxt(rel_path_and_file, dtype='float', delimiter=',', skip_header=self._skip_rows, skip_footer=self._skip_rows_footer, usecols=(self._xcolumn, self._ycolumn))

        # default value if plot_kwargs not client-supplied
        default = {'linewidth': 2.0, 'linestyle': '-'}
        self._plot_kwargs = kwargs.get('plot_kwargs', default)

        self._xscale = kwargs.get('xscale', 1.0)
        self._yscale = kwargs.get('yscale', 1.0)
        self._xoffset = kwargs.get('xoffset', 0.0)
        self._yoffset = kwargs.get('yoffset', 0.0)

        self._signal_process = kwargs.get('signal_process', None)

        if self._signal_process:
            for process_id in self._signal_process:
                process_dict = self._signal_process.get(process_id)
                key = next(iter(process_dict))
                value = process_dict[key]

                try:
                    method = getattr(self, key)
                    method(value)
                except AttributeError as error:
                    print(f'Error: invalid signal process key: {key}')
                    print(error.__class__.__name__)

                # process_module = module(f'{key}.process')
                # if process_module:
                #     process_object = getattr(process_module, 'Process')
                #     pobject = process_object(self._data, **value)
                #     # self._data[:, 1] = yfiltered  # overwrite y-axis now that it is filtered
                #     yfiltered = pobject.processed_data()
                #     self._data[:, 1] = yfiltered  # overwrite y-axis now that it is filtered

                # if key == 'butterworth':

                #     # process_module = import_module(f'{key}.process')
                #     # process_object = getattr(process_module, 'Process')


                #     fc = value.get('cutoff', None)  # Hz, cutoff frequency
                #     if fc is None:
                #         print('Error: keyword "cutoff" not found.')
                #         sys.exit('Abnormal termination.')

                #     filter_order = value.get('order', None)
                #     if filter_order is None:
                #         print('Error: keyword "order" not found.')
                #         sys.exit('Abnormal termination.')

                #     filter_type = value.get('type', None)
                #     if filter_type is None:
                #         print('Error: keyword "type" not found.')
                #         sys.exit('Abnormal termination.')

                #     print('Signal process ' + key + ' with:')
                #     print(f'  cutoff frequency = {fc} Hz')
                #     print(f'  filter order = {filter_order}')
                #     print('  filter type = ' + filter_type)

                #     dt = self._data[1, 0] - self._data[0, 0]  # sample delta t
                #     print(f'  sample delta t = {dt} seconds')

                #     fs = 1.0/dt  # Hz
                #     print(f'  sample frequency = {fs} Hz')

                #     Wn = fc / (fs / 2)  # normalized critical frequency
                #     print(f'  normalized critical frequency = {Wn} Hz/Hz')

                #     b, a = signal.butter(filter_order, Wn, filter_type)
                #     yfiltered = signal.filtfilt(b, a, self._data[:, 1])
                #     self._data[:, 1] = yfiltered  # overwrite

                #     serialize = value.get('serialize', 0)  # default is not to serialize
                #     if serialize:
                #         folder = value.get('folder', '.')  # default to current folder
                #         filename = value.get('file', str(process_id) + '.csv')

                #         #  abs_path = absolute_path(folder)
                #         #  # defaults to the process id
                #         #  abs_path_and_file = os.path.join(abs_path, filename)
                #         #  np.savetxt(abs_path_and_file, np.transpose([self._data[:, 0], self._data[:, 1]]), delimiter=',')
                #         #  print(f'  serialized file = {filename}')
                #         self.serialize(folder, filename)

                # elif key == 'gradient':

                #     gradient_order = value.get('order', None)
                #     if gradient_order is None:
                #         print('Error: keyword "order" not found.')
                #         sys.exit('Abnormal termination.')

                #     print('Signal process: ' + key + ' applied ' + str(gradient_order) + ' time(s)')
                #     # numerical gradient
                #     # https://docs.scipy.org/doc/numpy/reference/generated/numpy.gradient.html
                #     # for k in range(value):
                #     for k in range(gradient_order):
                #         ydot = np.gradient(self._data[:, 1], self._data[:, 0], edge_order=2)
                #         self._data[:, 1] = ydot  # overwrite
                #         print(f'  Derivative {k+1} completed.')

                #     serialize = value.get('serialize', 0)  # default is not to serialize
                #     if serialize:
                #         folder = value.get('folder', '.')  # default to current folder
                #         filename = value.get('file', str(process_id) + '.csv')

                #         # abs_path = absolute_path(folder)
                #         # # defaults to the process id
                #         # abs_path_and_file = os.path.join(abs_path, filename)
                #         # np.savetxt(abs_path_and_file, np.transpose([self._data[:, 0], self._data[:, 1]]), delimiter=',')
                #         # print(f'  serialized file = {filename}')
                #         self.serialize(folder, filename)

                # elif key == 'integration':

                #     integration_order = value.get('order', None)
                #     if integration_order is None:
                #         print('Error: keyword "order" not found.')
                #         sys.exit('Abnormal termination.')

                #     print('Signal process: ' + key + ' applied ' + str(integration_order) + ' time(s) with')

                #     default_ics = np.zeros(integration_order)
                #     ics = value.get('initial_conditions', default_ics)

                #     print(f'initial condition(s) as {ics}')

                #     if len(ics) != integration_order:
                #         print('Error: length of initial condition(s) array')
                #         print('must be equal to the order of integration.')
                #         print(f'Specified order = {integration_order}')
                #         print(f'Length of intial condition(s) array = {len(ics)}')
                #         sys.exit('Abnormal termination.')

                #     # https://docs.scipy.org/doc/numpy/reference/generated/numpy.trapz.html
                #     # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.integrate.cumtrapz.html
                #     for k in range(integration_order):
                #         # inty = np.trapz(self._data[:, 1], self._data[:, 0]) + ics[k]
                #         # inty = cumtrapz(self._data[:, 1], self._data[:, 0], initial=ics[k])
                #         inty = cumtrapz(self._data[:, 1], self._data[:, 0], initial=0) + ics[k]
                #         self._data[:, 1] = inty  # overwrite
                #         print(f'  Integral {k+1} completed.')

                #     serialize = value.get('serialize', 0)  # default is not to serialize
                #     if serialize:
                #         folder = value.get('folder', '.')  # default to current folder
                #         filename = value.get('file', str(process_id) + '.csv')

                #         self.serialize(folder, filename)

                # else:
                #     print('Error: Signal process key not implemented.')
                #     sys.exit('Abnormal termination.')

                print('  Signal process "' + key + '" completed.')

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

    def serialize(self, folder, filename):  # extend base class
        super().serialize(folder, filename)
        np.savetxt(self._path_file_output, np.transpose([self._data[:, 0], self._data[:, 1]]), delimiter=',')
        print(f'  Serialized model to: {self._path_file_output}')


    def butterworth(self, value):

        fc = value.get('cutoff', None)  # Hz, cutoff frequency
        if fc is None:
            print('Error: keyword "cutoff" not found.')
            sys.exit('Abnormal termination.')
        
        filter_order = value.get('order', None)
        if filter_order is None:
            print('Error: keyword "order" not found.')
            sys.exit('Abnormal termination.')
        
        filter_type = value.get('type', None)
        if filter_type is None:
            print('Error: keyword "type" not found.')
            sys.exit('Abnormal termination.')
        
        print('Signal process "butterworth" with:')
        print(f'  cutoff frequency = {fc} Hz')
        print(f'  filter order = {filter_order}')
        print('  filter type = ' + filter_type)
        
        dt = self._data[1, 0] - self._data[0, 0]  # sample delta t
        print(f'  sample delta t = {dt} seconds')
        
        fs = 1.0/dt  # Hz
        print(f'  sample frequency = {fs} Hz')
        
        Wn = fc / (fs / 2)  # normalized critical frequency
        print(f'  normalized critical frequency = {Wn} Hz/Hz')
        
        b, a = signal.butter(filter_order, Wn, filter_type)
        yfiltered = signal.filtfilt(b, a, self._data[:, 1])
        self._data[:, 1] = yfiltered  # overwrite
        
        serialize = value.get('serialize', 0)  # default is not to serialize
        if serialize:
            folder = value.get('folder', '.')  # default to current folder
            file_output = value.get('file', None)

            if file_output is None:
                print('Error: keyword "file" not found.')
                sys.exit('Abnormal termination.')
            else:
                self.serialize(folder, file_output)


    def gradient(self, value):

        gradient_order = value.get('order', None)
        if gradient_order is None:
            print('Error: keyword "order" not found.')
            sys.exit('Abnormal termination.')

        print('Signal process: "gradient" applied ' + str(gradient_order) + ' time(s)')
        # numerical gradient
        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.gradient.html
        # for k in range(value):
        for k in range(gradient_order):
            ydot = np.gradient(self._data[:, 1], self._data[:, 0], edge_order=2)
            self._data[:, 1] = ydot  # overwrite
            print(f'  Derivative {k+1} completed.')

        serialize = value.get('serialize', 0)  # default is not to serialize
        if serialize:
            folder = value.get('folder', '.')  # default to current folder
            file_output = value.get('file', None)

            if file_output is None:
                print('Error: keyword "file" not found.')
                sys.exit('Abnormal termination.')
            else:
                self.serialize(folder, file_output)

    def integration(self, value):

        integration_order = value.get('order', None)
        if integration_order is None:
            print('Error: keyword "order" not found.')
            sys.exit('Abnormal termination.')

        print('Signal process: "integration" applied ' + str(integration_order) + ' time(s) with')

        default_ics = np.zeros(integration_order)
        ics = value.get('initial_conditions', default_ics)

        print(f'initial condition(s) as {ics}')

        if len(ics) != integration_order:
            print('Error: length of initial condition(s) array')
            print('must be equal to the order of integration.')
            print(f'Specified order = {integration_order}')
            print(f'Length of intial condition(s) array = {len(ics)}')
            sys.exit('Abnormal termination.')

        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.trapz.html
        # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.integrate.cumtrapz.html
        for k in range(integration_order):
            # inty = np.trapz(self._data[:, 1], self._data[:, 0]) + ics[k]
            # inty = cumtrapz(self._data[:, 1], self._data[:, 0], initial=ics[k])
            inty = cumtrapz(self._data[:, 1], self._data[:, 0], initial=0) + ics[k]
            self._data[:, 1] = inty  # overwrite
            print(f'  Integral {k+1} completed.')

        serialize = value.get('serialize', 0)  # default is not to serialize
        if serialize:
            folder = value.get('folder', '.')  # default to current folder
            file_output = value.get('file', None)

            if file_output is None:
                print('Error: keyword "file" not found.')
                sys.exit('Abnormal termination.')
            else:
                self.serialize(folder, file_output)
