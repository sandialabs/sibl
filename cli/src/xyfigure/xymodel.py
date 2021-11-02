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


# Helper functions
def cross_correlation(reference, subject, verbose=False):

    if verbose:
        print("\nThis is xymodel.cross_correlation...")
        print(f"reference: {reference}")
        print(f"subject: {subject}")

    ref_delta_t = reference[1, 0] - reference[0, 0]
    ref_t_min = reference[0, 0]
    ref_t_max = reference[-1, 0]

    dt = subject[1, 0] - subject[0, 0]  # sample delta t
    t_min = subject[0, 0]
    t_max = subject[-1, 0]

    # globalized interval and frequency
    DT = np.minimum(ref_delta_t, dt)
    T_MIN = np.minimum(ref_t_min, t_min)
    T_MAX = np.maximum(ref_t_max, t_max)

    n_samples = int((T_MAX - T_MIN) / DT) + 1
    t_span = np.linspace(T_MIN, T_MAX, n_samples, endpoint=True)

    if verbose:
        print("\nSynchronization...")
        print(
            f"  Reference [t_min, t_max] by dt (s): [{ref_t_min}, {ref_t_max}] by {ref_delta_t}"
        )
        print(f"  Subject [t_min, t_max] by dt (s): [{t_min}, {t_max}] by {dt}")
        print(f"  Globalized [t_min, t_max] by dt (s): [{T_MIN}, {T_MAX}] by {DT}")
        print(f"  Globalized times: {t_span}")
        print(f"  Length of globalized times: {len(t_span)}")

    ref_y_span = np.interp(
        t_span, reference[:, 0], reference[:, 1], left=0.0, right=0.0
    )

    y_span = np.interp(t_span, subject[:, 0], subject[:, 1], left=0.0, right=0.0)

    cross_corr = np.correlate(ref_y_span, y_span, mode="full")
    cross_corr_max = np.max(cross_corr)

    cross_corr_unit = np.correlate(
        ref_y_span / np.linalg.norm(ref_y_span),
        y_span / np.linalg.norm(y_span),
        mode="full",
    )

    ref_self_corr = np.correlate(ref_y_span, ref_y_span)[0]  # self correlated reference
    rel_corr_error = 0.0

    if ref_self_corr > 0:
        rel_corr_error = abs(cross_corr_max - ref_self_corr) / ref_self_corr

    offset_index = np.argmax(cross_corr)

    # shift time full-left, then incrementally to the right
    # t_shift = t_span - t_span[-1] + t_span[offset_index]  # nope!
    # t_shift = t_span - t_span[-1] + offset_index * DT  # bug! should shift to t0 referance signal
    t_shift = t_span - t_span[-1] + t_span[0] + offset_index * DT

    T_MIN_CORR = np.minimum(ref_t_min, t_shift[0])
    T_MAX_CORR = np.maximum(ref_t_max, t_shift[-1])

    n_samples_corr = int((T_MAX_CORR - T_MIN_CORR) / DT) + 1  # DT unchanged pre-shift
    t_span_corr = np.linspace(T_MIN_CORR, T_MAX_CORR, n_samples_corr, endpoint=True)

    ref_y_span_corr = np.interp(
        t_span_corr, reference[:, 0], reference[:, 1], left=0.0, right=0.0
    )

    y_span_corr = np.interp(t_span_corr, t_shift, y_span, left=0.0, right=0.0)

    error = y_span_corr - ref_y_span_corr

    L2_norm_error_rate = np.linalg.norm(error) / n_samples_corr

    if verbose:
        print("\nCorrelation...")
        print(f"  Sliding dot product (cross-correlation): {cross_corr}")
        print(f"  Length of the sliding dot product: {len(cross_corr)}")
        print(f"  Max sliding dot product (cross-correlation): {cross_corr_max}")
        print(
            f"  Sliding dot product of normalized signals (cross-correlation): {cross_corr_unit}"
        )

        print(f"  Correlated time_shift (from full left)={offset_index * DT}")
        print(f"  Correlated index_shift (from full left)={offset_index}")

        print(f"  Correlated time step (s): {DT}")
        print(f"  Correlated t_min (s): {T_MIN_CORR}")
        print(f"  Correlated t_max (s): {T_MAX_CORR}")
        print(f"  Correlated times: {t_span_corr}")
        print(f"  Correlated reference f(t): {ref_y_span_corr}")
        print(f"  Correlated subject f(t): {y_span_corr}")
        print(f"  Correlated error f(t): {error}")

        print(f"  reference_self_correlation: {ref_self_corr}")
        print(f"  cross_correlation: {cross_corr_max}")
        print(f"    >> cross_correlation_relative_error={rel_corr_error}")
        print(f"    >> L2-norm error rate: {L2_norm_error_rate}")

    return t_span_corr, y_span_corr, rel_corr_error, L2_norm_error_rate


class XYModel(XYBase):
    """The data to be plotted in XY format."""

    def __init__(self, guid, **kwargs):
        super().__init__(guid, **kwargs)

        # TODO: rearchitect into single parent for both XYModel and XYModelAbaqus
        # make sure models have an input file that exists
        if not self._file_pathlib.is_file():
            print('Error: keyword "file" has a value (e.g., a file name):')
            print(self._file)
            print("with full path specification:")
            print(self._file_pathlib)
            raise KeyError("file not found")

        self._skip_rows = kwargs.get("skip_rows", 0)
        self._skip_rows_footer = kwargs.get("skip_rows_footer", 0)
        self._xcolumn = kwargs.get("xcolumn", 0)  # default to the 1st column
        self._ycolumn = kwargs.get("ycolumn", 1)  # default to the 2nd column

        # relative to current run location
        # rel_path_and_file = os.path.join(self._folder, self._file)
        # self._data = np.genfromtxt(
        #     rel_path_and_file,
        #     dtype="float",
        #     delimiter=",",
        #     skip_header=self._skip_rows,
        #     skip_footer=self._skip_rows_footer,
        #     usecols=(self._xcolumn, self._ycolumn),
        # )
        self._data = np.genfromtxt(
            self._path_file_input,
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

        verbosity = value.get("verbose", False)

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

        tcorrelated, ycorrelated, cc_relative_error, L2_error = cross_correlation(
            ref_data, self._data, verbose=verbosity
        )

        self._data = np.transpose([tcorrelated, ycorrelated])  # overwrite

        serialize = value.get("serialize", 0)  # default is not to serialize
        if serialize:
            folder = value.get("folder", ".")  # default to current folder
            file_output = value.get("file", None)

            if file_output is None:
                print('Error: keyword "file" not found.')
                sys.exit("Abnormal termination.")
            else:
                # self.serialize(folder, file_output, header=corr_str)
                self.serialize(folder, file_output)

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


class XYModelAbaqus(XYBase):
    """The ABAQUS mesh data to be plotted in XY format."""

    def __init__(self, guid, **kwargs):
        super().__init__(guid, **kwargs)

        # TODO: rearchitect into single parent for both XYModel and XYModelAbaqus
        # make sure models have an input file that exists
        if not self._file_pathlib.is_file():
            print('Error: keyword "file" has a value (e.g., a file name):')
            print(self._file)
            print("with full path specification:")
            print(self._file_pathlib)
            raise KeyError("file not found")

        with open(str(self._file_pathlib), "rt") as f:
            self._nodes = tuple()
            self._elements = tuple()
            # nice ref: https://www.pythontutorial.net/python-basics/python-read-text-file/
            try:
                # lines = f.readlines()

                # for line in f:
                line = f.readline()

                while line:
                    if "*NODE, " in line:
                        # collect all nodes
                        line = f.readline()  # get the next line
                        while "***" not in line:
                            line = line.split(",")
                            new_nodes = (
                                tuple([float(line[1]), float(line[2]), float(line[3])]),
                            )
                            self._nodes = self._nodes + new_nodes
                            # print(self._nodes)
                            line = f.readline()
                        # print(line)
                    elif "*ELEMENT, " in line:
                        # collect all elements
                        line = f.readline()  # get the next line
                        while len(line) > 0:
                            line = line.split(",")
                            new_element = (
                                tuple(
                                    [
                                        int(line[1]),
                                        int(line[2]),
                                        int(line[3]),
                                        int(line[4]),
                                    ]
                                ),
                            )
                            self._elements = self._elements + new_element
                            # print(self._elements)
                            line = f.readline()
                    else:
                        line = f.readline()

                print(f"Finished reading file: {self._file_pathlib}")

            except OSError:
                print(f"Cannot read file: {self._file_pathlib}")

        # default value if plot_kwargs not client-supplied
        # default = {"linewidth": 2.0, "linestyle": "solid", "color": "black", }
        default = {
            "linestyle": "dotted",
            "edgecolor": "magenta",
            "alpha": 0.8,
            "facecolor": "gray",
        }
        self._plot_kwargs = kwargs.get("plot_kwargs", default)
        self._linestyle = self._plot_kwargs.get("linestyle", "solid")
        self._edgecolor = self._plot_kwargs.get("edgecolor", "magenta")
        self._alpha = self._plot_kwargs.get("alpha", 0.8)
        self._facecolor = self._plot_kwargs.get("facecolor", "gray")

        aa = 4
