# Functional Architecture

from typing import NamedTuple, Tuple

import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path  # stop using os.path, use pathlib instead


class Database(NamedTuple):
    filename: str = "filename.ext"
    filetype: str = "ext"
    filepath: str = "."


class Csv(Database):
    filetype: str = "csv"


class Dsr(Database):
    filetype: str = "dsr"


class Cal(Database):
    filetype: str = "cal"


class Dat(Database):
    filetype: str = "dat"


class PairedLabels(NamedTuple):
    x: str = "x-axis"
    y: str = "y-axis"
    # x: str
    # y: str


class PairedSeries(NamedTuple):
    x: Tuple[float] = (0.0,)
    y: Tuple[float] = (0.0,)
    # x: Tuple[float]
    # y: Tuple[float]


class Figure(NamedTuple):
    labels: PairedLabels = PairedLabels()
    series: Tuple[PairedSeries] = (PairedSeries(),)
    xmin: float = 0.0
    xmax: float = 1.0
    ymin: float = 0.0
    ymax: float = 1.0
    filename: str = "figure.pdf"
    width: float = 8.0  # inches
    height: float = 6.0  # inches
    dpi: int = 150  # dots per inch, resolution


def csv_data_labels(x: Csv) -> PairedLabels:
    return PairedLabels()


def csv_data(x: Csv) -> PairedSeries:

    file_pathed = Path(x.filepath).joinpath(x.filename)

    data = np.genfromtxt(
        file_pathed, dtype="float", delimiter=",", skip_header=1, usecols=(0, 1)
    )
    return PairedSeries(x=tuple(data[:, 0]), y=tuple(data[:, 1]))


def dsr_data_labels(x: Dsr) -> PairedLabels:
    # return PairedLabels()
    raise NotImplementedError


def dsr_data(x: Dsr) -> PairedSeries:
    # return PairedSeries()
    raise NotImplementedError


def caldat_data_labels(x0: Cal, x1: Dat) -> PairedLabels:
    # return PairedLabels()
    raise NotImplementedError


def caldat_data(x0: Cal, x1: Dat) -> PairedSeries:
    # return PairedSeries()
    raise NotImplementedError


# def integrate(x0: PairedSeries, inital_condition: float = 0.0) -> PairedSeries:
def integrate(x0: PairedSeries, inital_condition: float) -> PairedSeries:
    return PairedSeries()


def differentiate(x: PairedSeries) -> PairedSeries:
    return PairedSeries()


# def butterworth_filter(
#     x0: PairedSeries, order: int = 4, type: str = "lowpass", cutoff: float = 1650.0
# ) -> PairedSeries:
def butterworth_filter(
    x0: PairedSeries, order: int, type: str, cutoff: float
) -> PairedSeries:
    return PairedSeries()


def figure_save(x: Figure) -> None:
    fig, ax = plt.subplots(nrows=1, dpi=x.dpi)
    fig.set_size_inches(w=x.width, h=x.height)

    for item in x.series:
        ax.plot(item.x, item.y)

    ax.set_xlim([x.xmin, x.xmax])
    ax.set_ylim([x.ymin, x.ymax])

    ax.grid()
    # ax.legend()
    fig.savefig(x.filename, dpi=x.dpi, bbox_inches="tight")
    print(f"  Saved figure as {x.filename}")
