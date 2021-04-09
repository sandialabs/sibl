"""This module uses imageio to concatenate sequence image files into movie."""

import imageio
from pygifsicle import optimize


base_name = "bspline_surface_biquad2tri_animation"

gif_path = base_name + ".gif"
gif_opt = base_name + "_opt.gif"
# frames_path = "{i}.jpg"
# bspline_surface_biquad2tri_animation.py0
# frames_path = "bspline_surface_biquad2tri_animation.py{i}.png"
frames_path = base_name + ".py{i}.png"
n = 21  # number of frames

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
