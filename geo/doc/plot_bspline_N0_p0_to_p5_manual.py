"""This module plots the first basis function for degree 0, 1, 2, 3, 4, 5.
"""

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rc

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
degrees = (0, 1)  # constant, linear, quadratic, etc.
# knot_vector = tuple(map(float, np.arange(degree + 2)))
# knot_vector = (0, 0, 1, 2, 2)
knot_vectors = ((0, 1), (0, 0, 1, 2, 2))
# coef = (0.0, 1.0, 0.0, 0.0, 0.0, 0.0)
# coef = (0.0, 1.0, 0.0, 0.0, 0.0)
# coef = (1.0, 0.0, 0.0, 0.0, 0.0)
coefs = ((1.0,), (0.0, 1.0, 0.0))
# coef = (
#     (0.0,),
#     (1.0,),
#     (0.0,),
# )

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
        label="$N_{0}^{" + str(i) + "}",
        linestyle=linestyles[np.remainder(i, len(linestyles))],
    )

ax.set_xlabel(r"$t$")
k = 0
# ax.set_ylabel(r"$N^{" + str(degree) + "}_{" + str(k) + "}(t)$")
ax.set_ylabel(r"$N^{p}_{" + str(k) + "}(t)$")

if display:
    plt.show()

if serialize:
    extension = ".pdf"  # or '.svg'
    bstring = "N(p=" + str(degree) + ")_" + str(k) + extension
    # fig.savefig(bstring, bbox_inches="tight")
    fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
