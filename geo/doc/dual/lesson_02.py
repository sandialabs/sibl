import math
import matplotlib.pyplot as plt


def main():

    n_samples = 40
    radius = 2.0

    # parameterize the curve
    ts = tuple(range(n_samples))

    # creates ts = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39

    # create x and y points
    xs = [radius * math.cos(2.0 * math.pi * t / n_samples) for t in ts]
    ys = [radius * math.sin(2.0 * math.pi * t / n_samples) for t in ts]

    s = 6.0  # 6.0 inches
    fig = plt.figure(figsize=(s, s))

    ax = fig.gca()

    ax.plot(xs, ys, "-", alpha=0.5)  # show boundary as a continuous connected line
    ax.plot(xs, ys, ".")  # show each discrete point that creates the boundary

    ax.set_aspect("equal")
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    plt.axis("on")

    plt.show()


if __name__ == "__main__":
    main()


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
