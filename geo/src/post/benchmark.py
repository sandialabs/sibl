"""
This module recreates the flower boundary representation presented in Figure 15 of
Rushdi AA, Mitchell SA, Mahmoud AH, Bajaj CC, Ebeida MS.
All-quad meshing without cleanup. Computer-Aided Design. 2017 Apr 1;85:83-98.

To run:
> cd ~/sibl
> conda activate siblenv
# update benchmark.py as needed
> python benchmark.py
"""
# from itertools import repeat
import math
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
from matplotlib import rc


def main():
    shown: Final = True
    serialize: Final = True

    latex: Final = False
    if latex:
        rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
        rc("text", usetex=True)

    test_case = "flower"  # "flower" | "default"

    if test_case == "flower":
        n_samples = 80
        radius = 2.0
        ts = tuple(range(n_samples + 1))
        rs = tuple(radius + 0.5 * math.cos(12.0 * math.pi * t / n_samples) for t in ts)
        xs = tuple(
            r * math.cos(radius * math.pi * t / n_samples) for (r, t) in zip(rs, ts)
        )
        ys = tuple(
            r * math.sin(radius * math.pi * t / n_samples) for (r, t) in zip(rs, ts)
        )
        ticks = list(range(-4, 5))
    else:
        n_samples = 40
        radius = 2.0
        ts = tuple(range(n_samples + 1))
        xs = tuple(radius * math.cos(2.0 * math.pi * t / n_samples) for t in ts)
        ys = tuple(radius * math.sin(2.0 * math.pi * t / n_samples) for t in ts)
        ticks = list(range(-4, 5))

    # parameter t
    # t = ()

    fig = plt.figure(figsize=(6.0, 6.0), dpi=100)
    ax = fig.gca()

    ax.plot(xs, ys, "-", alpha=0.5)
    ax.plot(xs, ys, ".")

    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    plt.axis("on")

    ax.set_xticks(ticks)
    ax.set_yticks(ticks)

    if shown:
        plt.show()

    if serialize:
        # cwd = Path.cwd()
        parent_path = Path(__file__).parent
        extension = ".pdf"  # ".png" | ".pdf" | ".svg"
        # filename = Path(__file__).stem + "_" + test_case + extension
        filename = test_case + extension
        # filepath = cwd.joinpath(filename)
        filepath = parent_path.joinpath(test_case, filename)
        fig.savefig(filepath, bbox_inches="tight", pad_inches=0)
        print(f"Serialized figure to {filepath}")

        extension = ".csv"


if __name__ == "__main__":
    main()
