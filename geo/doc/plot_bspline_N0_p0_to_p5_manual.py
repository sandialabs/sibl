"""This module plots the first basis function for degree 0, 1, 2, 3, 4, 5.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import MultipleLocator

import ptg.bspline as bsp

# degree = 0
display = True
dpi = 100  # dots per inch
latex = False
serialize = False
verbose = False

colors = ("tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:cyan")
linestyles = ("solid", "dashed", "dashdot")

if latex:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)

i = 0
# knot_vector = (0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0)  # num_knots = 7
# degree = 1  # constant
degrees = (0, 1, 2)  # constant, linear, quadratic, etc.
# knot_vector = tuple(map(float, np.arange(degree + 2)))
# knot_vector = (0, 0, 1, 2, 2)
knot_vectors = ((0, 1), (0, 0, 1, 2, 2), (0, 0, 0, 1, 2, 3, 3, 3))
# coef = (0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
# coef = (0.0, 1.0, 0.0, 0.0, 0.0)
# coef = (1.0, 0.0, 0.0, 0.0, 0.0)
coefs = ((1.0,), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0, 0.0, 0.0))
# coef = (
#     (0.0,),
#     (1.0,),
#     (0.0,),
# )
labels = ("$N_0^0$", "$N_0^1$", "$N_0^2$")

# fig = plt.figure(figsize=plt.figaspect(1.0 / (len(knot_vector) - 1)), dpi=dpi)
fig = plt.figure(figsize=plt.figaspect(1.0 / max(knot_vectors[-1])), dpi=dpi)
ax = fig.gca()
# ax.grid()
ax.grid(True, which="major", linestyle="-")
ax.grid(True, which="minor", linestyle=":")

for i in np.arange(len(degrees)):

    knot_vector = knot_vectors[i]
    coef = coefs[i]
    degree = degrees[i]
    label = labels[i]

    N0_p = bsp.Curve(knot_vector, coef, degree)
    result = N0_p.is_valid()

    n_bisections = 3  # 2^n_bisections
    npts = int((knot_vector[-1] - knot_vector[0]) * (2 ** n_bisections) + 1)
    # tmin, tmax, npts = knot_vector[0], knot_vector[-1], 13
    tmin, tmax, npts = knot_vector[0], knot_vector[-1], npts

    t = np.linspace(tmin, tmax, npts, endpoint=True)
    y = N0_p.evaluate(t)
    # y_known = (0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    # fig = plt.figure(figsize=plt.figaspect(1.0 / (len(knot_vector) - 1)), dpi=dpi)
    # ax = fig.gca()
    # # ax.grid()
    # ax.grid(True, which="major", linestyle="-")
    # ax.grid(True, which="minor", linestyle=":")
    # ax.scatter(t, y)
    ax.plot(
        t,
        y,
        "-*",
        linewidth=2,
        # label="$N_{0}^{" + str(i) + "}",
        label=label,
        linestyle=linestyles[np.remainder(i, len(linestyles))],
    )

ax.set_xlabel(r"$t$")
# ax.set_ylabel(r"$N^{" + str(degree) + "}_{" + str(k) + "}(t)$")
ax.set_ylabel(r"$N^{p\in[0,4]}_0(t)$")
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)

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
