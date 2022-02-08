"""This module creates the boundary for the quarter plate Hughes problem.

To run:
# Instead of:
> cd ~/sibl

# it is useful to navigate to the location of the quarter_plate.py file so that the
# output quarter_plate.txt file is written to the same location:
> ~/sibl/geo/data/boundary

> conda activate siblenv
> python quarter_plate.py

Reference: geometry/dual/code/bin/Release/forRyanHughes.m
"""

import math
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
import numpy as np


def main():
    shown: Final = True
    saved: Final = True

    radius: Final = 1.0

    ofile_name: Final = "quarter_plate.txt"

    # parameterize the curved portion of the boundary
    theta_min = 90  # degrees
    theta_max = 180  # degrees
    delta_theta = -1  # degrees
    # create a theta parameterization as [180, 175, 170, 95], not including 90 degrees
    thetas = tuple(range(theta_max, theta_min, delta_theta))
    arc_xs = tuple(radius * math.cos(t * math.pi / 180.0) for t in thetas)
    arc_ys = tuple(radius * math.sin(t * math.pi / 180.0) for t in thetas)

    # create the boundary in pieces in a counter-clockwise manner
    # starting from (-1, 0), to the left of the center of the hole
    #
    #                                    ^
    #                                    | y-axis
    #
    # pt4 = (-4, 4)  *----|----|----|----* pt3 = (0, 4)
    #                |                   |
    #                -                   -
    #                |                   |
    #                -                   -
    #                |                   |
    #                -                   * pt2 = (0, 1)
    #                |                /
    # pt0 = (-4, 0)  *----|----|----*    + whole center at (0, 0)  -> x-axis
    #                               pt1 = (-1, 0)

    n_samples = 1000

    east_xs = np.linspace(0, 0, n_samples)
    east_ys = np.linspace(1, 4, n_samples)

    north_xs = np.linspace(0, -4, n_samples)
    north_ys = np.linspace(4, 4, n_samples)

    west_xs = np.linspace(-4, -4, n_samples)
    west_ys = np.linspace(4, 0, n_samples)

    south_xs = np.linspace(-4, -1, n_samples)
    south_ys = np.linspace(0, 0, n_samples)

    xs = np.concatenate((arc_xs, east_xs, north_xs, west_xs, south_xs))
    ys = np.concatenate((arc_ys, east_ys, north_ys, west_ys, south_ys))

    if shown:
        size: Final = 6.0  # inches
        fig = plt.figure(figsize=(size, size))
        ax = fig.gca()

        # show boundary as a continuous connected line
        ax.plot(xs, ys, "-", alpha=0.5)

        # show each discrete point that creates the boundary
        ax.plot(xs, ys, ".")

        ax.set_aspect("equal")
        ax.set_xlabel(r"$x$")
        ax.set_ylabel(r"$y$")
        plt.show()

    if saved:
        # write the boundary pairs to a text file
        pathfile = Path(Path(__file__).parent, ofile_name)
        with open(file=pathfile, mode="w") as fout:
            for x, y in zip(xs, ys):
                fout.write(str(x) + "    " + str(y) + "\n")
            fout.close()
            print(f"Saved xy coordinates to file: {pathfile}")


if __name__ == "__main__":
    main()
