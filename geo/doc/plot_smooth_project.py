import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import MultipleLocator
from pathlib import Path

DISPLAY = True
LATEX = 0
SERIALIZE = False
N_SMOOTHS = 0

ox, oy = 0.0, 0.0  # offset for element labels

colors = (
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
    "tab:purple",
    "tab:brown",
    "tab:pink",
    "tab:gray",
    "tab:olive",
    "tab:cyan",
)

linestyles = ("solid", "dashed", "dashdot")


if LATEX:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)


def periodic_smooth(xs: tuple) -> tuple:
    x_shift_back = tuple((xs[-1],)) + xs[0 : len(xs) - 1]
    x_shift_forward = xs[1:] + tuple((xs[0],))
    x_mean = tuple(map(lambda x, y: 0.5 * (x + y), x_shift_back, x_shift_forward))
    return x_mean


x0, y0 = 0.0, 0.0  # center of circle
r = 5.0  # radius

n_elements = 16
t = np.linspace(0.0, 2.0 * np.pi, n_elements + 1)
t = t[:-1]  # drop the last t because we make the elements periodic below
xs = x0 + r * np.cos(t)
ys = y0 + r * np.sin(t)

nodes = np.transpose([xs, ys])
elements = [(i, i + 1) for i in range(len(nodes) - 1)] + [
    (len(nodes) - 1, 0)
]  # periodic

grid_size = 2.0  # characteristic grid side length

fence = (
    (5, 0),
    (5, 1),
    (5, 2),
    (5, 3),
    (4, 3),
    (4, 4),
    (3, 4),
    (3, 5),
    (2, 5),
    (1, 5),
    (0, 5),
    (-1, 5),
    (-2, 5),
    (-3, 5),
    (-3, 4),
    (-4, 4),
    (-4, 3),
    (-5, 3),
    (-5, 2),
    (-5, 1),
    (-5, 0),
    (-5, -1),
    (-5, -2),
    (-5, -3),
    (-4, -3),
    (-4, -4),
    (-3, -4),
    (-3, -5),
    (-2, -5),
    (-1, -5),
    (0, -5),
    (1, -5),
    (2, -5),
    (3, -5),
    (3, -4),
    (4, -4),
    (4, -3),
    (5, -3),
    (5, -2),
    (5, -1),
)
xsf = tuple(i[0] for i in fence)
ysf = tuple(i[1] for i in fence)

for smooth in range(N_SMOOTHS + 1):

    fig = plt.figure(figsize=(4, 4))
    ax = fig.gca()
    # ax.grid()
    # ax.plot(
    #     xs,
    #     ys,
    #     "-",
    #     linewidth=2,
    # )

    for e, element in enumerate(elements):
        print(f"element {e}")
        color = colors[np.remainder(e, len(colors))]
        xs_e = [nodes[n, 0] for n in element]
        ys_e = [nodes[n, 1] for n in element]
        ax.plot(
            xs_e,
            ys_e,
            linewidth=2,
            color=color,
            linestyle=linestyles[np.remainder(e, len(linestyles))],
        )
        # draw in elements as an element number with a circle
        ax.annotate(
            str(e),
            xy=(np.average(xs_e) + ox, np.average(ys_e) + oy),
            xycoords="data",
            bbox={"boxstyle": "circle", "color": color, "alpha": 0.2},
            horizontalalignment="center",
            verticalalignment="center",
        )

    ax.plot(xsf, ysf, "o-", linewidth=1, color="red", alpha=0.5)

    xsf = periodic_smooth(xsf)  # overwrite for next time through loop
    ysf = periodic_smooth(ysf)

    # ax.plot(xsf2, ysf2, "o-", linewidth=1, color="orange", alpha=0.5)

    ax.grid(True, which="major", linestyle="-")
    ax.grid(True, which="minor", linestyle=":")

    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$y$")

    ax.set_title(f"smooths = {smooth}")

    ax.set_aspect("equal")

    ax.xaxis.set_major_locator(MultipleLocator(1.0))
    # ax.xaxis.set_minor_locator(MultipleLocator(0.5))
    ax.yaxis.set_major_locator(MultipleLocator(1.0))
    # ax.yaxis.set_minor_locator(MultipleLocator(0.5))

    if DISPLAY:
        plt.show()

    if SERIALIZE:
        extension = ".pdf"  # or '.svg'
        bstring = Path(__file__).stem + "_smooth_" + str(smooth) + extension
        # fig.savefig(bstring, bbox_inches="tight")
        fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
        print(f"Serialized file to {bstring}")
