"""This module creates the boundary for the donut problem.

To run:
# Instead of:
> cd ~/sibl

# it is useful to navigate to the location of the donut.py file so that the
# output donut.txt file is written to the same location:
> cd ~/sibl/geo/data/boundary

> conda activate siblenv
> python donut.py
"""

import math
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt


def main():
    shown: Final = False
    saved: Final = True

    radius_inner: Final = 3.25
    radius_outer: Final = 8.0

    ofile_name: Final = "donut.txt"

    # parameterize the curve
    theta_min = 0  # degrees
    theta_max = 360  # degrees
    delta_theta = 5  # degrees
    # create a theta parameterization as [0, 5, 10, ... 360]
    thetas = tuple(range(theta_min, theta_max, delta_theta))

    # the outer circle progresses clockwise
    outer_xs = tuple(radius_outer * math.cos(t * math.pi / 180.0) for t in thetas)
    outer_ys = tuple(radius_outer * math.sin(t * math.pi / 180.0) for t in thetas)

    # the inner circle progresses counter-clockwise
    inner_xs = tuple(
        radius_inner * math.cos(t * math.pi / 180.0) for t in reversed(thetas)
    )
    inner_ys = tuple(
        radius_inner * math.sin(t * math.pi / 180.0) for t in reversed(thetas)
    )

    # collect the two boundary curves
    xs = outer_xs + ("NaN",) + inner_xs
    ys = outer_ys + ("NaN",) + inner_ys

    if shown:
        size: Final = 6.0  # inches
        fig = plt.figure(figsize=(size, size))
        ax = fig.gca()

        # show outer boundary as a continuous connected line
        ax.plot(outer_xs, outer_ys, "-", alpha=0.5)

        # show each discrete point that creates the outer boundary
        ax.plot(outer_xs, outer_ys, ".")

        # show inner boundary as a continuous connected line
        ax.plot(inner_xs, inner_ys, "-", alpha=0.5)

        # show each discrete point that creates the inner boundary
        ax.plot(inner_xs, inner_ys, ".")

        plt.grid()

        ax.set_aspect("equal")
        plt.show()

    if saved:
        # write the boundary pairs to a text file
        with open(file=ofile_name, mode="w") as fout:
            for x, y in zip(xs, ys):
                fout.write(str(x) + "    " + str(y) + "\n")
            fout.close()
            pathfile = Path(ofile_name).resolve()
            print(f"Saved xy coordinates to file: {pathfile}")


if __name__ == "__main__":
    main()
