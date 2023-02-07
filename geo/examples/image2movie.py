"""This module uses imageio to concatenate sequence image files into movie."""

import imageio
from pygifsicle import optimize


# base_name = "bspline_surface_biquad2tri_animation"
# base_name = "bspline_surface_cyl2sphere_animation"
# base_name = "mesh_smoothing_iter_"
# base_name = "lesson_04b_iter_"
base_name = "lesson_04c_iter_"

gif_path = base_name + ".gif"
gif_opt = base_name + "_opt.gif"
# frames_path = "{i}.jpg"
# frames_path = base_name + "{i}.png"
frames_path = base_name + "{i:03d}.png"

# bspline_surface_biquad2tri_animation.py0
# frames_path = "bspline_surface_biquad2tri_animation.py{i}.png"
# frames_path = base_name + ".py{i}.png"

# number of frames
n = 19
# n = 6  # number of frames
# n = 21  # number of frames

with imageio.get_writer(gif_path, mode="I") as writer:
    # morph forward from initial state to final state
    for i in range(n):
        writer.append_data(imageio.imread(frames_path.format(i=i)))

    # run in reverse direction to visualize "undo" of the morph
    # morph from final state back to initial state
    for i in reversed(range(n)):
        writer.append_data(imageio.imread(frames_path.format(i=i)))

# optimize(gif_path, "optimized.gif")  # For creating a new one
optimize(gif_path, gif_opt)  # For creating a new one
# optimize(gif_path) # For overwriting the original one


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
