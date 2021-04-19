# Functional Architecture

from typing import NamedTuple, Tuple

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


class PairedSeries(NamedTuple):
    x: Tuple[float] = (0.0,)
    y: Tuple[float] = (0.0,)


class FigureBase(NamedTuple):
    labels: PairedLabels = PairedLabels()
    series: Tuple[PairedSeries] = (PairedSeries(),)
    xmin: float = 0.0
    xmax: float = 1.0
    ymin: float = 0.0
    ymax: float = 1.0
    type: str = "pdf"


class FigureMPL(FigureBase):
    width: float = 8.0  # inches
    height: float = 6.0  # inches
    dpi: int = 150  # dots per inch, resolution


def csv_data_labels(x: Csv) -> PairedLabels:
    return PairedLabels()


def csv_data(x: Csv) -> PairedSeries:

    file_pathed = Path.joinpath(x.filepath, x.filename)

    data = np.genfromtxt(
        file_pathed, dtype="float", delimiter=",", skip_header=1, usecols=(0, 1)
    )
    return PairedSeries(x=tuple(data[:, 0]), y=tuple(data[:, 1]))


def dsr_data_labels(x: Dsr) -> PairedLabels:
    return PairedLabels()


def dsr_data(x: Dsr) -> PairedSeries:
    return PairedSeries()


def caldat_data_labels(x0: Cal, x1: Dat) -> PairedLabels:
    return PairedLabels()


def caldat_data(x0: Cal, x1: Dat) -> PairedSeries:
    return PairedSeries()


def integrate(x0: PairedSeries, inital_condition: float = 0.0) -> PairedSeries:
    return PairedSeries()


def differentiate(x: PairedSeries) -> PairedSeries:
    return PairedSeries()


def filter(
    x0: PairedSeries, order: int = 4, type: str = "lowpass", cutoff: float = 1650.0
) -> PairedSeries:
    return PairedSeries()
