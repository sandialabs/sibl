"""This module plots periodic B-spline quadratic basis functions.

Example:
> cd ~/sibl/geo/doc
> conda activate siblenv
> python plot_periodic_bspline_basis_p2.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import MultipleLocator

display = True
dpi = 100  # dots per inch
latex = True  #  False
n_bisections = 6  # 2^n_bisections
serialize = False

colors = ("tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:cyan")
linestyles = ("solid", "dashed", "dashdot")

if latex:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)

# bases = (0, 1, 2)  # three basis functions
t = np.linspace(0, 1, 2 ** n_bisections + 1)
# b = tuple(t)
# a = tuple(map(lambda x: 1.0 - x, b))
# a = np.array(tuple(map(lambda t: 1.0 - t, t)))
# b = t

# n0 = 0.5 * a * a * a
# n1 = 1.5 * (a * a * b + 5 * a * b * b) + 0.5
# n2 = 0.5 * b * b * b

N0 = np.array(tuple(map(lambda t: 0.5 * (1.0 - t) ** 2, t)))
N1 = np.array(
    tuple(map(lambda t: 0.5 * (1.0 - t) ** 2 + 2 * t * (1.0 - t) + 0.5 * t ** 2, t))
)
N2 = np.array(tuple(map(lambda t: 0.5 * t ** 2, t)))

bases = (N0, N1, N2)
labels = (r"$\tilde{N}_0^2$", r"$\tilde{N}_1^2$", r"$\tilde{N}_2^2$")

# fig = plt.figure(figsize=plt.figaspect(1.0 / 1.0), dpi=dpi)
fig = plt.figure()
ax = fig.gca()

for i, base in enumerate(bases):
    # y = bases[i]
    label = labels[i]
    ax.plot(
        t,
        base,
        "-",
        linewidth=2,
        label=label,
        linestyle=linestyles[np.remainder(i, len(linestyles))],
    )

ax.grid(True, which="major", linestyle="-")
ax.grid(True, which="minor", linestyle=":")

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$\tilde{N}^{p=2}_i(t)$")
# ax.legend(loc="upper right")
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

_eps = 0.1
ax.set_xlim([0.0 - 2 * _eps, 1.0 + 2 * _eps])
ax.set_ylim([0.0 - 2 * _eps, 1.0 + 2 * _eps])

ax.set_aspect("equal")

ax.xaxis.set_major_locator(MultipleLocator(1.0))
ax.xaxis.set_minor_locator(MultipleLocator(0.25))
ax.yaxis.set_major_locator(MultipleLocator(1.0))
ax.yaxis.set_minor_locator(MultipleLocator(0.25))

if display:
    plt.show()

if serialize:
    extension = ".pdf"  # or '.svg'
    bstring = "N_0_p=0to4" + extension
    # fig.savefig(bstring, bbox_inches="tight")
    fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
