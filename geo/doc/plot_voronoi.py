"""This module creates a Voroni diagram from a sequence of 2D seed points.

Example:
Example (interactive):
> cd ~/sibl/geo/doc
> conda activate siblenv
> python plot_voronoi.py
"""
# import argparse
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.ticker import MultipleLocator
from scipy.spatial import Voronoi, voronoi_plot_2d

# seeds = np.array(
#     [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
# )
# seeds = ((0, 0), (0.5, 0), (1, 0), (0, 0.5), (0.5, 0.5), (0, 1), (1, 1))
a = 0.5
h = 0.5 * np.sqrt(2.0)
i = 1.25
b = a * np.sqrt(2.0) / 2.0
# seeds = ((0, 0), (a, 0), (2 * a, 0), (0, a), (a, a), (0, 2 * a), (2 * a, 2 * a))
# seeds = ((0, 0), (a, 0), (2 * a, 0), (0, a), (b, b), (0, 2 * a), (2 * b, 2 * b))
seeds = (
    (0, 0),
    (a, 0),
    (0, a),
    (h * i * a, h * i * a),
    (2 * a, 0),
    (0, 2 * a),
    (2 * h * a, 2 * h * a),
)

vor = Voronoi(seeds)
fig = voronoi_plot_2d(vor)
# fig = plt.figure()
ax = fig.gca()
# ax.grid()
# ax.grid(True, which="major", linestyle="-")
# ax.grid(True, which="minor", linestyle=":")

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
# ax.legend(loc="upper right")

# _eps = 0.1
# ax.set_xlim([-1.0 - 2 * _eps, 1.0 + 2 * _eps])
# ax.set_ylim([-1.0 - 2 * _eps, 1.0 + 2 * _eps])

ax.set_aspect("equal")
# plt.axis("equal)")

ax.xaxis.set_major_locator(MultipleLocator(1.0))
ax.xaxis.set_minor_locator(MultipleLocator(0.25))
ax.yaxis.set_major_locator(MultipleLocator(1.0))
ax.yaxis.set_minor_locator(MultipleLocator(0.25))

plt.show()

# The example from the documentation
rng = np.random.default_rng()
points = rng.random((10, 2))

vor = Voronoi(points)
fig = voronoi_plot_2d(vor)
# fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='orange', line_width=2, line_alpha=0.6, point_size=2)
plt.show()


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
