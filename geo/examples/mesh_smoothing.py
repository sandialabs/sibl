# Lesson: Mesh Smoothing

"""
Goals:

* Demonstrate how to use mesh smoothing in SIBL
* Demonstrate mesh smoothing characteristics
"""

# Minimum Working Example (MWE) mesh with four elements

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import ptg.mesh as mesh
import ptg.mesh_smoothing as smooth

"""
* Construct a four-element mesh with non-sequential node numbers and elements numbers, for generality.
* Use pinned boundary conditions at the four corners:
  * `101`, `103`, `13`, `33`
* Use roller boundary conditions on the four edges:
  * `2`, `4`, `6`, `23`
* Note that roller boundary condition nodes and node `105` are perterbed from their original grid-like positions.

^ y-axis
|
|       13       23       33 (3.0, 3.0)
         *--------*--------*
         |        |        |
         |  (44)  |  (31)  |
         |        |105     |
       4 *--------*--------* 6
         |        |        |
         |   (1)  |  (20)  |
         |        |        |
         *--------*--------*
        101       2       103
     (1.0, 1.0)

+ --> x-axis
"""


def sum_of_deltas_L2_norm(*, displacements):
    sum = 0.0
    for key, value in displacements.items():
        sum += np.linalg.norm(value)
    # print(f"Sum of L2 norm of displacements: {sum}")
    return sum


self_path_file = Path(__file__)
self_path = self_path_file.resolve().parent
data_path = self_path.joinpath("../", "data", "mesh").resolve()
input_mesh_file = data_path.joinpath("four_quads_nonseq.inp")
script_name = Path(__file__).stem

nodes = mesh.inp_path_file_to_coordinates(pathfile=str(input_mesh_file))

elements = mesh.inp_path_file_to_connectivities(pathfile=str(input_mesh_file))

elements_wo_element_number = tuple([x[1:] for x in elements])

edges = mesh.adjacencies_upper_diagonal(xs=elements_wo_element_number)

mesh_dict = {
    "title": "Initial Configuration",
    "node_numbers_shown": False,
    "serialize": True,
    "basename": script_name,
}
_ = mesh.plot_mesh(nodes=nodes, edges=edges, options=mesh_dict)

boundary = mesh.inp_path_file_to_boundary(pathfile=str(input_mesh_file))

# Do a single mesh smoothing iteration and plot the updated configuration
deltas = smooth.smooth_neighbor_nonweighted(
    nodes=nodes, elements=elements, boundary=boundary, update_ratio=0.5
)

sum = sum_of_deltas_L2_norm(displacements=deltas)

updated_configuration = {}
for key, value in nodes.items():
    updated_configuration[key] = np.array(nodes[key]) + np.array(deltas[key])

mesh_dict["title"] = "Updated Configuration"  # overwrite
mesh.plot_mesh(nodes=updated_configuration, edges=edges, options=mesh_dict)

# Do k mesh smoothing iterations
ur = 0.1  # update ratio
n_iterations = 100
plot_interval = 1

# The k=0 iteration is the initial configuration
configuration_k = {}

for key, value in nodes.items():
    configuration_k[key] = np.array(nodes[key])

mesh_dict["title"] = "Iteration k=0"
mesh_dict["basename"] = script_name + "_iter_000"
mesh.plot_mesh(nodes=configuration_k, edges=edges, options=mesh_dict)

iteration_hx = []
L2_hx = []
converged = False
tolerance = 0.01
k = 0

# for k in range(1, n_iterations + 1):
while k <= n_iterations and not converged:
    k += 1

    deltas_k = smooth.smooth_neighbor_nonweighted(
        nodes=configuration_k, elements=elements, boundary=boundary, update_ratio=ur
    )
    L2 = sum_of_deltas_L2_norm(displacements=deltas_k)
    iteration_hx.append(k)
    L2_hx.append(L2)

    L2_str = format(L2, "e")
    title_str = f"Iter k={k}, " + L2_str

    # overwrite old configuration with updated configuration
    for key, value in configuration_k.items():
        configuration_k[key] += deltas_k[key]

    if L2 <= tolerance:
        converged = True

    if not (k % plot_interval):
        mesh_dict["title"] = "Iteration k=" + str(k)
        iter_str_3_digit = f"{k:03d}"
        mesh_dict["basename"] = script_name + "_iter_" + iter_str_3_digit
        mesh.plot_mesh(nodes=configuration_k, edges=edges, options=mesh_dict)


fig = plt.figure(figsize=(3.0, 3.0), dpi=100)
ax = fig.gca()

plt.plot(iteration_hx, L2_hx, ".--")
plt.grid(True)
ax.set_xlabel("iteration (k)")
ax.set_ylabel("sum L2(u)")
ax.set_title("Convergence")

if mesh_dict["serialize"]:
    filename = script_name + "_convergence" + ".png"
    pathfilename = Path.cwd().joinpath(filename)
    fig.savefig(pathfilename, bbox_inches="tight", pad_inches=0)
    print(f"Serialized to {pathfilename}")

plt.plot(iteration_hx, L2_hx, ".--")
plt.yscale("log")
plt.grid(True)
ax.set_xlabel("iteration (k)")
ax.set_ylabel("sum L2(u)")
ax.set_title("Convergence")

if mesh_dict["serialize"]:
    filename = script_name + "_convergence_log" + ".png"
    pathfilename = Path.cwd().joinpath(filename)
    fig.savefig(pathfilename, bbox_inches="tight", pad_inches=0)
    print(f"Serialized to {pathfilename}")
