import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rc

# from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator

# import bspline_polynomial as bp
# import ptg.bspline_polynomial as bp
import ptg.bspline as bsp

# (siblenv) [~/sibl/geo/doc] python plot_bspline.py

DEGREE = 2  # 0 constant, 1 linear, 2 quadratic, 3 cubic
DISPLAY = 1
DPI = 100  # dots per inch
KNOT_OFFSET = 0
LATEX = 0
NBI = 5  # number of bisections per knot interval
NCP = 9  # number of control points
SERIALIZE = 0
VERBOSE = 0

linestyles = ["solid", "dashed", "dashdot"]
num_linestyles = len(linestyles)

if LATEX:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)

# e.g., p=0 constant, p=1 linear, p=2 quadratic, p=3 cubic

# knot_vector = [-1, 0, 1, 2, 3, 4, 5]
# knot_vector = [0, 1, 2, 3, 4, 5, 6]
a, b = 0, NCP - DEGREE
knot_vector = (
    np.concatenate((np.repeat(a, DEGREE), np.arange(a, b), np.repeat(b, DEGREE + 1)))
    + KNOT_OFFSET
)

# number of elements is the number of non-zero knot spans
num_elements = len(np.unique(knot_vector)) - 1

print(f"Computing B-spline with bases of degree={DEGREE}")
print(f"with knot vector {knot_vector}")
print(f"with number of bisections per knot interval={NBI}")
print(f"with number of elements (non-zero knot spans)={num_elements}")

knots_lhs = knot_vector[0:-1]  # left-hand-side knot values
knots_rhs = knot_vector[1:]  # right-hand-side knot values
knot_spans = np.array(knots_rhs) - np.array(knots_lhs)
dt = knot_spans / (2 ** NBI)
assert all([dti >= 0 for dti in dt]), "Error: knot vector is decreasing."

num_knots = len(knot_vector)
t = [
    knots_lhs[k] + j * dt[k]
    for k in np.arange(num_knots - 1)
    for j in np.arange(2 ** NBI)
]
t.append(knot_vector[-1])
t = np.array(t)
N = []

# for k in np.arange(len(knot_vector) - 1 - DEGREE):
for i in np.arange(NCP):

    # coef = np.zeros(len(knot_vector) - (DEGREE + 1))
    coef = np.zeros(NCP)
    # coef[k] = 1.0
    coef[i] = 1.0

    B = bsp.BSpline(knot_vector, coef, DEGREE)

    if B.is_valid():
        y = B.evaluate(t)

        N.append(y)


# fig = plt.figure(figsize=plt.figaspect(1.0 / (num_knots - 1)), dpi=DPI)
fig = plt.figure(figsize=plt.figaspect(1.0 / (num_elements + 1)), dpi=DPI)
ax = fig.gca()
# ax.grid()
# ax.grid(True, which="both")  # both major and minor grid to on
ax.grid(True, which="major", linestyle="-")
ax.grid(True, which="minor", linestyle=":")

# ax.plot(t, y, linestyle="None", marker=".")
for i in np.arange(NCP):
    ax.plot(
        t,
        N[i],
        "-",
        lw=2,
        label=f"$N_{i}^{DEGREE}$",
        linestyle=linestyles[np.remainder(i, num_linestyles)],
    )

ax.set_xlabel(r"$t$")
# ax.set_ylabel(r"$N^{p}_{i}(t)$")
ax.set_ylabel(f"$N^{DEGREE}_i(t)$")

eps = 0.1
ax.set_xlim([knot_vector[0] - 2 * eps, knot_vector[-1] + 2 * eps])
# ax.set_xlim([0.0 - 2 * eps, 6.0 + 2 * eps])
ax.set_ylim([0.0 - 2 * eps, 1.0 + 2 * eps])
ax.set_aspect("equal")
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
# ax.xaxis.set_minor_locator(MultipleLocator(0.5))
ax.xaxis.set_major_locator(MultipleLocator(1.0))
ax.xaxis.set_minor_locator(MultipleLocator(0.5))
# ax.xaxis.set_major_locator(MultipleLocator(1.0))
ax.yaxis.set_major_locator(MultipleLocator(1.0))
ax.yaxis.set_minor_locator(MultipleLocator(0.5))
# ax.set_xticklabels(["1", "", "2"])


if DISPLAY:
    plt.show()

if SERIALIZE:
    extension = ".pdf"  # or '.svg'
    # bstring = "N(p=" + str(DEGREE) + ")_" + str(k) + extension
    bstring = "N(p=" + str(DEGREE) + ")_i" + extension
    # fig.savefig(bstring, bbox_inches="tight")
    fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
