"""This module is a baseline registration and investigation into the output form of the
active contour model (aka snakes) in the scikit-image library.

Reference: https://scikit-image.org/docs/stable/auto_examples/edges/plot_active_contours.html#sphx-glr-auto-examples-edges-plot-active-contours-py

The active contour model is a method to fit open or closed splines to lines or edges in an image 1. It works by minimising an energy that is in part defined by the image and part by the spline’s shape: length and smoothness. The minimization is done implicitly in the shape energy and explicitly in the image energy.

In the following two examples the active contour model is used (1) to segment the face of a person from the rest of an image by fitting a closed curve to the edges of the face and (2) to find the darkest curve between two fixed points while obeying smoothness considerations. Typically it is a good idea to smooth images a bit before analyzing, as done in the following examples.

We initialize a circle around the astronaut's face and use the default boundary condition boundary_condition='periodic' to fit a closed curve. The default parameters w_line=0, w_edge=1 will make the curve search towards edges, such as the boundaries of the face.

1. Snakes: Active contour models. Kass, M.; Witkin, A.; Terzopoulos, D. International Journal of Computer Vision 1 (4): 321 (1988). DOI:10.1007/BF00133570
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour
from skimage.draw import circle

# from skimage.draw import circle_perimeter

show_astro = True
show_circle = False
serialize = True

if show_astro:
    img = (
        data.astronaut()
    )  # Eileen Collins https://en.wikipedia.org/wiki/Eileen_Collins
    # orginal image is 512 x 512 x 3 = 786,432 ints
    # 3-channel (r, g, b) each channel [0, 255]

    img = rgb2gray(img)
    # color -> grayscale
    # grayscale image is 512 x 512 = 262,144 ints

    n_samples_circumerference = 400
    theta = np.linspace(
        0, 2 * np.pi, n_samples_circumerference
    )  # theta.shape is (400,)
    x0, y0, radius = 220, 100, 100  # pixels
    rows = y0 + radius * np.sin(theta)
    cols = x0 + radius * np.cos(theta)

    init = np.array([rows, cols]).T

    # Reference: https://scikit-image.org/docs/stable/api/skimage.segmentation.html#active-contour
    # Source: https://github.com/scikit-image/scikit-image/blob/v0.18.0/skimage/segmentation/active_contour_model.py
    snake = active_contour(gaussian(img, 3), init, alpha=0.015, beta=10, gamma=0.001)
    # grayscale gaussian filtered image is 512 x 512 = 262,144 ints
    # snake.shape is (400, 2)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(img, cmap=plt.cm.gray)
    ax.plot(
        init[:, 1], init[:, 0], linestyle="dashed", color="red", linewidth=3, alpha=0.7
    )
    ax.plot(
        snake[:, 1],
        snake[:, 0],
        linestyle="solid",
        color="blue",
        linewidth=3,
        alpha=0.7,
    )
    # ax.set_xticks([]), ax.set_yticks([])
    # ax.axis([0, img.shape[1], img.shape[0], 0])

    plt.show()

    # example from https://github.com/scikit-image/scikit-image/blob/v0.18.0/skimage/segmentation/active_contour_model.py

if show_circle:
    # create image
    n_pixels = 100
    img = np.zeros((n_pixels, n_pixels), dtype=np.uint8)
    # Reference: https://scikit-image.org/docs/dev/api/skimage.draw.html?highlight=circle_perimeter#skimage.draw.circle_perimeter
    x0, y0, radius = 35, 45, 25
    # rr, cc = circle_perimeter(35, 25, 25)
    # rr, cc = circle_perimeter(x0, y0, radius)
    rr, cc = circle(r=x0, c=y0, radius=radius)

    # smooth image
    img[rr, cc] = 1  # perimeter mask
    n_smoothings = 2
    img_smoothed = gaussian(img, n_smoothings)

    # initialize spline
    s = np.linspace(0, 2 * np.pi, 100)
    # snake initialization is circle touching the outer border of the complete pixel snan
    init = 0.5 * n_pixels * np.array([np.sin(s), np.cos(s)]).T + 50

    # snake = active_contour(img_smoothed, init, w_edge=0, w_line=1, coordinates="rc")
    snake = active_contour(img_smoothed, init)
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(6, 2), sharex=True, sharey=True)

    ax = axes.ravel()

    ax[0].imshow(img, cmap=plt.cm.gray)
    ax[0].axis("image")
    ax[0].set_title("original")

    ax[1].imshow(img_smoothed, cmap=plt.cm.gray)
    ax[1].axis("image")
    ax[1].set_title("Gauss smoothings: " + str(n_smoothings))

    ax[2].imshow(img_smoothed, cmap=plt.cm.gray)
    ax[2].axis("image")
    ax[2].set_title("snakes")

    ax[2].plot(
        init[:, 1], init[:, 0], linestyle="dashed", color="red", linewidth=3, alpha=0.7
    )
    ax[2].plot(
        snake[:, 1],
        snake[:, 0],
        linestyle="solid",
        color="blue",
        linewidth=3,
        alpha=0.7,
    )

    fig.tight_layout()
    plt.show()

if serialize:
    extension = ".png"  # ".pdf"  # or '.svg'
    bstring = Path(__file__).stem + extension
    # fig.savefig(bstring, bbox_inches="tight")
    fig.savefig(bstring, bbox_inches="tight", pad_inches=0)
    print(f"Serialized file to {bstring}")


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
