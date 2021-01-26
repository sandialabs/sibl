import math
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from PIL import Image
from skimage import data
from skimage import transform

# tform = transform.SimilarityTransform(scale=1, rotation=math.pi / 2, translation=(0, 1))
# print(tform.params)

# text = data.text()
#
# tform = transform.SimilarityTransform(
#     scale=1, rotation=math.pi / 4, translation=(text.shape[0] / 2, -100)
# )
#
# rotated = transform.warp(text, tform)
# back_rotated = transform.warp(rotated, tform.inverse)
#
# fig, ax = plt.subplots(nrows=3)
#
# ax[0].imshow(text, cmap=plt.cm.gray)
# ax[1].imshow(rotated, cmap=plt.cm.gray)
# ax[2].imshow(back_rotated, cmap=plt.cm.gray)
#
# for a in ax:
#     a.axis("off")
#
# plt.tight_layout()
# plt.show()

# example 2
#
# text = data.text()
#
# # ordered, quadrant I, II, III, IV
# src = np.array([[300, 50], [0, 50], [0, 0], [300, 0]])
# dst = np.array([[260, 130], [65, 40], [155, 15], [360, 95]])
#
# tform3 = transform.ProjectiveTransform()
# tform3.estimate(src, dst)
# warped = transform.warp(text, tform3, output_shape=(50, 300))
#
# fig, ax = plt.subplots(nrows=2, figsize=(8, 3))
#
# ax[0].imshow(text, cmap=plt.cm.gray)
# ax[0].plot(dst[:, 0], dst[:, 1], ".r")
# ax[1].imshow(warped, cmap=plt.cm.gray)
#
# plt.tight_layout
# plt.show()


# _script_file = Path(__file__)
# _script_dir = _script_file.resolve().parent
# _image_path = Path.joinpath(_script_dir, "chevy_license.png")
# _image_path = Path.joinpath("geo/tests", "chevy_license.png")
_image_path = "geo/tests/chevy_license.png"

# pil_image = Image.open("chevy_license.png", "r")
pil_image = Image.open(_image_path, "r")
width, height = pil_image.size

# image coordinate system
#
#   origin (0, 0)  *------------> x-axis and u-axis (columns)
#                  |  tl.    tr.
#                  |                 four points in the top-left, top-right,
#                  |  bl.    br.        bottom-left,
#                  v
#     y-axis and v-axis (rows)

fig, ax = plt.subplots(nrows=2, figsize=(8, 4))

source_tr = (782, 154)  # pixels
source_tl = (556, 154)
source_bl = (558, 246)
source_br = (781, 250)
source_x = (source_tr[0], source_tl[0], source_bl[0], source_br[0], source_tr[0])
source_y = (source_tr[1], source_tl[1], source_bl[1], source_br[1], source_tr[1])
dst = np.transpose([source_x, source_y])

target_tr = (800, 200)  # pixels
target_tl = (600, 200)
target_bl = (600, 300)
target_br = (800, 300)
target_x = np.array(
    (target_tr[0], target_tl[0], target_bl[0], target_br[0], target_tr[0])
)
target_y = np.array(
    (target_tr[1], target_tl[1], target_bl[1], target_br[1], target_tr[1])
)
target = np.transpose([target_x, target_y])

pixel_values = np.array(pil_image.getdata())  # convert from list to numpy array
n_pixels = len(pixel_values)

if pil_image.mode == "RGBA":
    channels = 4
    # map RGB to black and white per Hovey 2013, equation (25); ignore alpha channel
    pixel_image = (
        0.2989 * pixel_values[:, 0]
        + 0.5879 * pixel_values[:, 1]
        + 0.1140 * pixel_values[:, 2]
    )
elif pil_image.mode == "RGB":
    channels = 3
    pixel_image = (
        0.2989 * pixel_values[:, 0]
        + 0.5879 * pixel_values[:, 1]
        + 0.1140 * pixel_values[:, 2]
    )
elif pil_image.mode == "L":
    channels = 1
else:
    print(f"Unknown Python Image Library mode: {pil_image.mode}")
    # return None

pixel_image = pixel_image.reshape((height, width))


tform3 = transform.ProjectiveTransform()
# tform3.estimate(src, dst)
# tform3.estimate(src, dst)
tform3.estimate(target, dst)

# warped = transform.warp(pixel_values, tform3, output_shape=(100, 200))
# warped = transform.warp(pixel_values, tform3)
# warped = transform.warp(pixel_image, tform3, output_shape=(1000, 2000))
warped = transform.warp(pixel_image, tform3)


# ax[0].imshow(pil_image, cmap=plt.cm.gray)
ax[0].imshow(pil_image)
ax[0].plot(source_x, source_y, marker="o", color="orange", linewidth=1, alpha=0.5)
ax[1].imshow(warped, cmap=plt.cm.gray)
ax[1].plot(target_x, target_y, marker="+", color="red", linewidth=1, alpha=0.5)
n_shifts = 3
for i in np.arange(n_shifts):
    ax[1].plot(
        target_x[0:-3] - (i + 1) * 200,
        target_y[0:-3],
        marker="+",
        color="magenta",
        linewidth=1,
        linestyle="dashed",
        alpha=0.4,
    )

plt.tight_layout
plt.show()
