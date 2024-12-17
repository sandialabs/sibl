"""Tests if two images are the same on a pixel-by-pixel basis.

    Typical use case:
    $ python image_diff.py image_a image_b
"""

# https://www.python.org/dev/peps/pep-0008/#imports
# standard library imports
import sys

# related third-party imports
import numpy as np
from PIL import Image


def same(file_a, file_b, verbose=0):
    """Determines if two images are the same or different.

    Creates to image files from the image string arguments, then gets the
    pixel data from each image.  Subtracts pixel information of file_b from
    file_a, and creates a numpy array, which is the pixel-by-pixel difference
    of the two images.

    If the L2 norm of the difference array is less than a small tolerance, the
    two images are classified as the same.  Otherwise, they are classified as
    different.

    Args:
        file_a (string) The first of two image file names.
        file_b (string): The second of two image file names.
        verbose: (Boolean): True is more command line feedback than False.

    Returns:
        Boolean:  True for images are the same; False for images are different.
    """

    same_xy_dimension = False
    same_mode = False
    same_channels = False
    same_pixels = False

    if verbose:  # pragma: no cover
        print(f"Image 1 file name: {file_a}")
        print(f"Image 2 file name: {file_b}")

    try:
        with Image.open(file_a) as im_a, Image.open(file_b) as im_b:

            im_a_size = im_a.size
            im_b_size = im_b.size

            same_xy_dimension = im_a_size == im_b_size

            if verbose:  # pragma: no cover
                print("Test 1 of 2: Dimensionality comparison")
                print(f"  (x,y) dimension of image 1 is {im_a_size}")
                print(f"  (x,y) dimension of image 2 is {im_b_size}")

            same_mode = im_a.mode == im_b.mode

            if same_xy_dimension and same_mode:

                data_a = np.array(im_a.getdata()).flatten()
                data_b = np.array(im_b.getdata()).flatten()

                same_channels = data_a.size == data_b.size

                if same_channels:
                    data_diff = data_a - data_b

                    data_diff_norm = np.linalg.norm(data_diff)

                    # tolerance for the L2norm to be same or different
                    image_tol = 10.0

                    same_pixels = np.abs(data_diff_norm) < image_tol

                    if verbose:  # pragma: no cover
                        print("  Images (x,y) have same dimensions? [T/F]:")
                        print(f"{same_xy_dimension}")

                        print(f"  Images have same mode? [T/F]: {same_mode}")
                        print("  Images have same number of channels? [T/F]:")
                        print(f"{same_channels}")

                        print("Test 2 of 2: Pixel-by-pixel comparison")
                        print(f"  Size of data image 1 is {data_a.size}")
                        print(f"  Size of data image 2 is {data_b.size}")
                        print(f"  Pixels are the same? [T/F]: {same_pixels}")

            else:  # pragma: no cover
                if verbose:
                    print("  Images (x,) have same dimensions? [T/F]:")
                    print(f"{same_xy_dimension}")

                    print(f"  Images have same mode? [T/F]: {same_mode}")

                    print("  Images have same number of channels? [T/F]:")
                    print(f"{same_channels}")

                    print("Images are different.")

            if verbose:  # pragma: no cover
                print(f"Returning {same_pixels}")

            return same_pixels

    except IOError:
        print("Error: could not open files:")
        print(f"  {file_a}")
        print(f"  {file_b}")


def main(argv):
    """The main entry point for command line interation.

    Reads two image file string from the command line arguments and forward
    the file name strings to the worker method called 'same()'.

    Args:
        file_a: The first of two image file names.
        file_b: The second of two image file names.

    Returns:
        None
    """

    try:
        file_a = argv[0]
        file_b = argv[1]
    except IndexError as error:
        print(f"Error: {error}.")
        print("Abnormal script termination.")
        sys.exit("Two image files must be specified as arguments.")

    same(file_a, file_b, verbose=True)


if __name__ == "__main__":
    main(sys.argv[1:])


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
