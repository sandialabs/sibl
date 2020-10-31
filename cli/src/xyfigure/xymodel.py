# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports
import os
import sys

# related third-party imports
import numpy as np
from scipy import signal
from scipy.integrate import cumtrapz

# local application/library specific imports
# from xyfigure.xybase import XYBase
# from xyfigure.code.xybase import XYBase
from xyfigure.xybase import XYBase, absolute_path


class XYModel(XYBase):
    """The data to be plotted in XY format."""

    def __init__(self, guid, **kwargs):
        super().__init__(guid, **kwargs)

        self._skip_rows = kwargs.get("skip_rows", 0)
        self._skip_rows_footer = kwargs.get("skip_rows_footer", 0)
        self._xcolumn = kwargs.get("xcolumn", 0)  # default to the 1st column
        self._ycolumn = kwargs.get("ycolumn", 1)  # default to the 2nd column

        rel_path_and_file = os.path.join(
            self._folder, self._file
        )  # relative to current run location
        self._data = np.genfromtxt(
            rel_path_and_file,
            dtype="float",
            delimiter=",",
            skip_header=self._skip_rows,
            skip_footer=self._skip_rows_footer,
            usecols=(self._xcolumn, self._ycolumn),
        )

        # default value if plot_kwargs not client-supplied
        default = {"linewidth": 2.0, "linestyle": "-"}
        self._plot_kwargs = kwargs.get("plot_kwargs", default)

        self._xscale = kwargs.get("xscale", 1.0)
        self._yscale = kwargs.get("yscale", 1.0)
        self._xoffset = kwargs.get("xoffset", 0.0)
        self._yoffset = kwargs.get("yoffset", 0.0)

        self._signal_process = kwargs.get("signal_process", None)

        if self._signal_process:
            for process_id in self._signal_process:
                process_dict = self._signal_process.get(process_id)
                key = next(iter(process_dict))
                value = process_dict[key]

                try:
                    method = getattr(self, key)
                    method(value)
                except AttributeError as error:
                    print(f"Error: invalid signal process key: {key}")
                    print(error.__class__.__name__)

                if self._verbose:
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

    def serialize(self, folder, filename, header=""):  # extend base class
        super().serialize(folder, filename)
        np.savetxt(
            self._path_file_output,
            np.transpose([self._data[:, 0], self._data[:, 1]]),
            delimiter=",",
            header=header,
        )
        if self._verbose:
            print(f"  Serialized model to: {self._path_file_output}")

    def butterworth(self, value):

        fc = value.get("cutoff", None)  # Hz, cutoff frequency
        if fc is None:
            print('Error: keyword "cutoff" not found.')
            sys.exit("Abnormal termination.")

        filter_order = value.get("order", None)
        if filter_order is None:
            print('Error: keyword "order" not found.')
            sys.exit("Abnormal termination.")

        filter_type = value.get("type", None)
        if filter_type is None:
            print('Error: keyword "type" not found.')
            sys.exit("Abnormal termination.")

        if self._verbose:
            print('Signal process "butterworth" with:')
            print(f"  cutoff frequency = {fc} Hz")
            print(f"  filter order = {filter_order}")
            print("  filter type = " + filter_type)

        dt = self._data[1, 0] - self._data[0, 0]  # sample delta t

        if self._verbose:
            print(f"  sample delta t = {dt} seconds")

        fs = 1.0 / dt  # Hz
        if self._verbose:
            print(f"  sample frequency = {fs} Hz")

        Wn = fc / (fs / 2)  # normalized critical frequency
        if self._verbose:
            print(f"  normalized critical frequency = {Wn} Hz/Hz")

        b, a = signal.butter(filter_order, Wn, filter_type)
        yfiltered = signal.filtfilt(b, a, self._data[:, 1])
        self._data[:, 1] = yfiltered  # overwrite

        serialize = value.get("serialize", 0)  # default is not to serialize
        if serialize:
            folder = value.get("folder", ".")  # default to current folder
            file_output = value.get("file", None)

            if file_output is None:
                print('Error: keyword "file" not found.')
                sys.exit("Abnormal termination.")
            else:
                self.serialize(folder, file_output)

    def correlation(self, value):

        reference = value.get("reference", None)
        if reference is None:
            print('Error: keyword "reference" not found.')
            sys.exit("Abnormal termination.")

        # ref is the reference signal to compare with
        ref_default_folder = "."
        ref_folder = reference.get("folder", ref_default_folder)

        ref_file = reference.get("file", None)

        if ref_file is None:
            print('Error: keyword "file" not found.')
            sys.exit("Abnormal termination.")

        abs_path = absolute_path(ref_folder)
        ref_path_file_input = os.path.join(abs_path, ref_file)

        ref_skip_rows = reference.get("skip_rows", 0)
        ref_skip_rows_footer = reference.get("skip_rows_footer", 0)
        ref_xcolumn = reference.get("xcolumn", 0)  # default to the 1st column
        ref_ycolumn = reference.get("ycolumn", 1)  # default to the 2nd column

        ref_data = np.genfromtxt(
            ref_path_file_input,
            dtype="float",
            delimiter=",",
            skip_header=ref_skip_rows,
            skip_footer=ref_skip_rows_footer,
            usecols=(ref_xcolumn, ref_ycolumn),
        )

        ref_delta_t = ref_data[1, 0] - ref_data[0, 0]
        ref_t_min = ref_data[0, 0]
        ref_t_max = ref_data[-1, 0]

        dt = self._data[1, 0] - self._data[0, 0]  # sample delta t
        t_min = self._data[0, 0]
        t_max = self._data[-1, 0]

        # globalized interval and frequency
        T_MIN = np.minimum(ref_t_min, t_min)
        T_MAX = np.maximum(ref_t_max, t_max)
        DT = np.minimum(ref_delta_t, dt)

        n_samples = int((T_MAX - T_MIN) / DT) + 1
        t_span = np.linspace(T_MIN, T_MAX, n_samples, endpoint=True)

        ref_y_span = np.interp(
            t_span, ref_data[:, 0], ref_data[:, 1], left=0.0, right=0.0
        )

        y_span = np.interp(
            t_span, self._data[:, 0], self._data[:, 1], left=0.0, right=0.0
        )

        cross_corr = np.correlate(ref_y_span, y_span, mode="full")
        cross_corr_max = np.max(cross_corr)

        ref_self_corr = np.correlate(ref_y_span, ref_y_span)[0]
        rel_corr_error = 0.0

        if ref_self_corr > 0:
            rel_corr_error = abs(cross_corr_max - ref_self_corr) / ref_self_corr

        offset_index = np.argmax(cross_corr)

        t_shift = t_span - t_span[-1] + t_span[offset_index]

        self._data = np.transpose([t_shift, y_span])  # overwrite

        corr_str = f"time_shift={t_span[offset_index]}"
        corr_str += f" index_shift={offset_index}"
        corr_str += f" cross_correlation_relative_error={rel_corr_error}"

        serialize = value.get("serialize", 0)  # default is not to serialize
        if serialize:
            folder = value.get("folder", ".")  # default to current folder
            file_output = value.get("file", None)

            if file_output is None:
                print('Error: keyword "file" not found.')
                sys.exit("Abnormal termination.")
            else:
                self.serialize(folder, file_output, header=corr_str)

    def gradient(self, value):

        gradient_order = value.get("order", None)
        if gradient_order is None:
            print('Error: keyword "order" not found.')
            sys.exit("Abnormal termination.")

        if self._verbose:
            print(
                "Signal process:"
                "  gradient applied " + str(gradient_order) + " time(s)"
            )
        # numerical gradient
        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.gradient.html
        # for k in range(value):
        for k in range(gradient_order):
            ydot = np.gradient(self._data[:, 1], self._data[:, 0], edge_order=2)
            self._data[:, 1] = ydot  # overwrite
            if self._verbose:
                print(f"  Derivative {k+1} completed.")

        serialize = value.get("serialize", 0)  # default is not to serialize
        if serialize:
            folder = value.get("folder", ".")  # default to current folder
            file_output = value.get("file", None)

            if file_output is None:
                print('Error: keyword "file" not found.')
                sys.exit("Abnormal termination.")
            else:
                self.serialize(folder, file_output)

    def integration(self, value):

        integration_order = value.get("order", None)
        if integration_order is None:
            print('Error: keyword "order" not found.')
            sys.exit("Abnormal termination.")

        print(
            'Signal process: "integration" applied '
            + str(integration_order)
            + " time(s) with"
        )

        default_ics = np.zeros(integration_order)
        ics = value.get("initial_conditions", default_ics)

        print(f"initial condition(s) as {ics}")

        if len(ics) != integration_order:
            print("Error: length of initial condition(s) array")
            print("must be equal to the order of integration.")
            print(f"Specified order = {integration_order}")
            print(f"Length of intial condition(s) array = {len(ics)}")
            sys.exit("Abnormal termination.")

        # https://docs.scipy.org/doc/numpy/reference/generated/numpy.trapz.html
        # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.integrate.cumtrapz.html
        for k in range(integration_order):
            # inty = np.trapz(self._data[:, 1], self._data[:, 0]) + ics[k]
            # inty = cumtrapz(self._data[:, 1], self._data[:, 0], initial=ics[k])
            inty = cumtrapz(self._data[:, 1], self._data[:, 0], initial=0) + ics[k]
            self._data[:, 1] = inty  # overwrite
            print(f"  Integral {k+1} completed.")

        serialize = value.get("serialize", 0)  # default is not to serialize
        if serialize:
            folder = value.get("folder", ".")  # default to current folder
            file_output = value.get("file", None)

            if file_output is None:
                print('Error: keyword "file" not found.')
                sys.exit("Abnormal termination.")
            else:
                self.serialize(folder, file_output)
