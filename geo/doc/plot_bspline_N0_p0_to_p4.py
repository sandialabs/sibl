"""This module plots the first basis function for degree 0, 1, 2, 3, 4, 5.

Example:
> cd ~/sibl/geo/doc
> conda activate siblenv
> python plot_bspline_N0_p0_to_p4.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import MultipleLocator

import ptg.bspline as bsp

# degree = 0
display = True
dpi = 100  # dots per inch
latex = True  # False
n_bisections = 4  # 2^n_bisections
serialize = True  # False

colors = ("tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple", "tab:cyan")
linestyles = ("solid", "dashed", "dashdot")

if latex:
    rc("font", **{"family": "serif", "serif": ["Computer Modern Roman"]})
    rc("text", usetex=True)

degrees = (0, 1, 2, 3, 4)  # constant, linear, quadratic, etc.
knot_vectors = (
    (0, 1),
    (0, 0, 1, 2, 2),
    (0, 0, 0, 1, 2, 3, 3, 3),
    (0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4),
    (0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 5, 5, 5, 5),
)
coefs = (
    (1.0,),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0, 0.0, 0.0),
    (0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0),
    (0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0),
)
labels = ("$N_0^0$", "$N_0^1$", "$N_0^2$", "$N_0^3$", "$N_0^4$")

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

    npts = int((knot_vector[-1] - knot_vector[0]) * (2**n_bisections) + 1)
    # tmin, tmax, npts = knot_vector[0], knot_vector[-1], 13
    tmin, tmax, npts = knot_vector[0], knot_vector[-1], npts

    t = np.linspace(tmin, tmax, npts, endpoint=True)
    y = N0_p.evaluate(t)
    ax.plot(
        t,
        y,
        "-",
        linewidth=2,
        label=label,
        linestyle=linestyles[np.remainder(i, len(linestyles))],
    )

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$N^{p\in[0,4]}_0(t)$")
ax.legend(loc="upper right")

_eps = 0.1
ax.set_xlim([knot_vectors[-1][0] - 2 * _eps, knot_vectors[-1][-1] + 2 * _eps])
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
