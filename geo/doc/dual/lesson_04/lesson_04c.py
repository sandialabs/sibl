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

elements_as_vertices = mesh.faces_as_nodes_to_faces_as_vertices(
    faces=elements_wo_element_number, coordinates=nodes
)
elements_2D_as_vertices = tuple(
    tuple((x, y) for (x, y, z) in element) for element in elements_as_vertices
)

basename = script_name + "_manual_iter_0"

fig_dict = {
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

# Now, the connecitivity in the .inp file is CW, which is exactly reversed of
# the CCW convention, so apply `reversed` on all element connectivities
# when computing the scaled Jacobian.
min_scaled_js_pre_smooth = tuple(
    mesh.minimum_scaled_jacobian_of_quad(vertices=tuple(reversed(element)))
    for element in elements_2D_as_vertices
)
# Plot the histogram of minimum scaled Jacobians
fig = plt.figure(figsize=(fig_dict["width"], fig_dict["height"]), dpi=fig_dict["dpi"])
ax_hist = fig.gca()
n_bins = 40
delta_bin = 1.0 / n_bins
bins = [delta_bin * x for x in range(n_bins + 1)]
pre_smooth_kwargs = {"alpha": 0.6, "color": "black"}
post_smooth_kwargs = {"histtype": "step", "alpha": 0.9, "linewidth": 2, "color": "blue"}

rgb_gray = (0.6, 0.6, 0.6)
rgb_blue = (0.0, 0.0, 1.0)

plt.hist(
    min_scaled_js_pre_smooth,
    bins=bins,
    label="binned pre-smooth",
    **pre_smooth_kwargs,
)

plt.xlabel("Minimum Scaled Jacobian")
plt.ylabel("Number of Elements")
plt.title("Element Minimum Scaled Jacobians Pre-Smoothing")
hist_x = [0.6, 1.0]
hist_y = [0.6, 60]
plt.xlim(hist_x)
plt.ylim(hist_y)
ax_hist.legend(loc="upper left")
plt.grid(True)

plt.show()

edges = mesh.adjacencies_upper_diagonal(xs=elements_wo_element_number)

# suppress plotting mesh since it is now redundant to the k smoothing plots
# mesh.plot_mesh(nodes=nodes, edges=edges, options=fig_dict)

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
fig_dict["basename"] = basename  # overwrite
fig_dict["title"] = "Updated Configuration"  # overwrite

# suppress plotting mesh since it is now redundant to the k smoothing plots
# mesh.plot_mesh(nodes=updated_configuration, edges=edges, options=fig_dict)

# Now do k mesh smoothing iterations
ur = 0.25  # update ratio
n_iterations = 20
# plot_interval = 18
plot_interval = 1

# The k=0 iteration is the initial configuration
configuration_k = {}

for key, value in nodes.items():
    configuration_k[key] = np.array(nodes[key])

fig_dict["title"] = "Iteration k=0"
fig_dict["basename"] = script_name + "_iter_000"
fig_dict["color"] = rgb_gray
mesh.plot_mesh(nodes=configuration_k, edges=edges, options=fig_dict)

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
        fig_dict["title"] = "Iteration k=" + str(k)
        iter_str_3_digit = f"{k:03d}"
        fig_dict["basename"] = script_name + "_iter_" + iter_str_3_digit
        fig_dict["color"] = (1.0 - k / n_iterations) * np.array(rgb_gray) + (
            k / n_iterations
        ) * np.array(rgb_blue)
        mesh.plot_mesh(nodes=configuration_k, edges=edges, options=fig_dict)

        # Plot the histogram of minimum scaled Jacobians
        elements_as_vertices_smoothed = mesh.faces_as_nodes_to_faces_as_vertices(
            faces=elements_wo_element_number, coordinates=configuration_k
        )
        elements_2D_as_vertices_smoothed = tuple(
            tuple((x, y) for (x, y, z) in element)
            for element in elements_as_vertices_smoothed
        )

        min_scaled_js_post_smooth = tuple(
            mesh.minimum_scaled_jacobian_of_quad(vertices=tuple(reversed(element)))
            for element in elements_2D_as_vertices_smoothed
        )

        fig = plt.figure(
            figsize=(fig_dict["width"], fig_dict["height"]), dpi=fig_dict["dpi"]
        )
        ax = fig.gca()

        plt.hist(
            min_scaled_js_pre_smooth,
            bins=bins,
            label="binned pre-smooth",
            **pre_smooth_kwargs,
        )
        plt.hist(
            min_scaled_js_post_smooth,
            bins=bins,
            label="binned post-smooth",
            **post_smooth_kwargs,
        )

        plt.xlabel("Minimum Scaled Jacobian")
        plt.ylabel("Number of Elements")
        plt.title("Element Minimum Scaled Jacobians Pre- and Post-Smoothing")
        plt.xlim(hist_x)
        plt.ylim(hist_y)
        ax.legend(loc="upper left")
        plt.grid(True)
        plt.show()

        if fig_dict["serialize"]:
            filename = script_name + "_histogram" + ".png"
            pathfilename = Path.cwd().joinpath(filename)
            fig.savefig(pathfilename, bbox_inches="tight", pad_inches=0)
            print(f"Serialized to {pathfilename}")


fig = plt.figure(figsize=(3.0, 3.0), dpi=100)
ax = fig.gca()

plt.plot(iteration_hx, L2_hx, ".--")
plt.grid(True)
ax.set_xlabel("iteration (k)")
ax.set_ylabel("sum L2(u)")
ax.set_title("Convergence")

if fig_dict["serialize"]:
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

if fig_dict["serialize"]:
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
