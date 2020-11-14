import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rc

# from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MultipleLocator

# import bspline_polynomial as bp
# import ptg.bspline_polynomial as bp
import ptg.bspline as bsp

# (siblenv) [~/sibl/geo/doc] python plot_bspline_basis.py

config_recover_Bezier_linear = {
    "degree": 1,
    "ncp": 2,
}

config_recover_Bezier_quadratic = {
    "degree": 2,
    "nbi": 7,
    "ncp": 3,
}

config_recover_Bezier_cubic = {
    "degree": 3,
    "nbi": 7,
    "ncp": 4,
}

config_recover_Bezier_quartic = {
    "degree": 4,
    "nbi": 7,
    "ncp": 5,
}

config_Cottrell_Fig2p5 = {
    "degree": 2,
    "nbi": 7,
    "ncp": 8,
    "knot_vector": [0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 5],
}

config_Cottrell_Fig2p6 = {
    "degree": 4,
    "nbi": 7,
    "ncp": 15,
    "knot_vector": [0, 0, 0, 0, 0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5],
}

# config = config_recover_Bezier_linear
# config = config_recover_Bezier_quadratic
# config = config_recover_Bezier_cubic
# config = config_recover_Bezier_quartic
config = config_Cottrell_Fig2p5
# config = config_Cottrell_Fig2p6

DEGREE = config.get("degree", 0)  # 0 constant, 1 linear, 2 quadratic, 3 cubic
DISPLAY = config.get("display", True)  # show to screen
DPI = config.get("dpi", 100)  # dots per inch
KNOT_OFFSET = config.get("knot_offset", 0)  # translate knot vector to left or right
LATEX = config.get("latex", False)  # use LaTeX instead of default fonts
NBI = config.get("nbi", 2)  # number of bisections per knot interval
NCP = config.get("ncp", 2)  # number of control points
SERIALIZE = config.get("serialize", False)  # save figure to disc
VERBOSE = config.get("verbose", False)

linestyles = ["solid", "dashed", "dashdot"]
num_linestyles = len(linestyles)

if LATEX:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)

a, b = 0, NCP - DEGREE
knot_vector = (
    np.concatenate((np.repeat(a, DEGREE), np.arange(a, b), np.repeat(b, DEGREE + 1)))
    + KNOT_OFFSET
)
KV = config.get(
    "knot_vector", knot_vector
)  # default is open vector, no internal knot multiplicity

# number of elements is the number of non-zero knot spans
num_elements = len(np.unique(KV)) - 1

print(f"Computing B-spline basis with degree={DEGREE}")
print(f"with knot vector {KV}")
print(f"of {len(KV)} knots")
print(f"with number of bisections per knot interval={NBI}")
print(f"with number of elements (non-zero knot spans)={num_elements}")

knots_lhs = KV[0:-1]  # left-hand-side knot values
knots_rhs = KV[1:]  # right-hand-side knot values
knot_spans = np.array(knots_rhs) - np.array(knots_lhs)
dt = knot_spans / (2 ** NBI)
assert all([dti >= 0 for dti in dt]), "Error: knot vector is decreasing."

num_knots = len(KV)
t = [
    knots_lhs[k] + j * dt[k]
    for k in np.arange(num_knots - 1)
    for j in np.arange(2 ** NBI)
]
t.append(KV[-1])
t = np.array(t)
N = []

for i in np.arange(NCP):

    coef = np.zeros(NCP)
    coef[i] = 1.0

    B = bsp.BSpline(KV, coef, DEGREE)

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

for i in np.arange(NCP):
    CPTXT = f"{i}"
    DEGTXT = f"{DEGREE}"
    ax.plot(
        t,
        N[i],
        "-",
        lw=2,
        label="$N_{" + CPTXT + "}^{" + DEGTXT + "}$",
        linestyle=linestyles[np.remainder(i, num_linestyles)],
    )

ax.set_xlabel(r"$t$")
ax.set_ylabel(f"$N^{DEGREE}_i(t)$")

eps = 0.1
ax.set_xlim([KV[0] - 2 * eps, KV[-1] + 2 * eps])
ax.set_ylim([0.0 - 2 * eps, 1.0 + 2 * eps])
ax.set_aspect("equal")
ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.0)
ax.xaxis.set_major_locator(MultipleLocator(1.0))
ax.xaxis.set_minor_locator(MultipleLocator(0.25))
ax.yaxis.set_major_locator(MultipleLocator(1.0))
ax.yaxis.set_minor_locator(MultipleLocator(0.25))


if DISPLAY:
    plt.show()

if SERIALIZE:
    extension = ".pdf"  # or '.svg'
    # bstring = "N(p=" + str(DEGREE) + ")_" + str(k) + extension
    bstring = "N(p=" + str(DEGREE) + ")_NCP=" + str(NCP) + extension
    # fig.savefig(bstring, bbox_inches="tight")
    fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
