# Goal: demonstrate mesh smoothing on existing mesh

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import ptg.mesh as mesh
import ptg.mesh_morph as morph


def sum_of_deltas_L2_norm(*, displacements):
    sum = 0.0
    for key, value in displacements.items():
        sum += np.linalg.norm(value)
    # print(f"Sum of L2 norm of displacements: {sum}")
    return sum


script_name = Path(__file__).stem
script_path = Path(__file__).parent
input_mesh_file = script_path.joinpath("lesson_04_mesh_w_boundary.inp")

nodes = mesh.inp_path_file_to_coordinates(pathfile=str(input_mesh_file))

elements = mesh.inp_path_file_to_connectivities(pathfile=str(input_mesh_file))

elements_wo_element_number = tuple([x[1:] for x in elements])

edges = mesh.adjacencies_upper_diagonal(xs=elements_wo_element_number)

basename = script_name + "_manual_iter_0"

mesh_dict = {
    "title": "Initial Configuration",
    "node_numbers_shown": False,
    "nodes_shown": False,
    "height": 6.0,
    "width": 6.0,
    "dpi": 200,
    "serialize": True,
    "basename": basename,
    "figure_shown": True,
}
# suppress plotting mesh since it is now redundant to the k smoothing plots
# mesh.plot_mesh(nodes=nodes, edges=edges, options=mesh_dict)

boundary = mesh.inp_path_file_to_boundary(pathfile=str(input_mesh_file))

# Do a single mesh smoothing iteration and plot the updated configuration
deltas = morph.smooth_neighbor_nonweighted(
    nodes=nodes, elements=elements, boundary=boundary, update_ratio=0.5
)

sum = sum_of_deltas_L2_norm(displacements=deltas)

updated_configuration = {}
for key, value in nodes.items():
    updated_configuration[key] = np.array(nodes[key]) + np.array(deltas[key])

basename = script_name + "_manual_iter_1"  # overwrite
mesh_dict["basename"] = basename  # overwrite
mesh_dict["title"] = "Updated Configuration"  # overwrite

# suppress plotting mesh since it is now redundant to the k smoothing plots
# mesh.plot_mesh(nodes=updated_configuration, edges=edges, options=mesh_dict)

# Now do k mesh smoothing iterations
ur = 0.25  # update ratio
n_iterations = 20
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
tolerance = 0.1
k = 0

# for k in range(1, n_iterations + 1):
while k <= n_iterations and not converged:
    k += 1

    deltas_k = morph.smooth_neighbor_nonweighted(
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
