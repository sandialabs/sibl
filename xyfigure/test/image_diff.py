"""Tests if two images are the same on a pixel-by-pixel basis.

    Typical useage example:
    $ python image_diff.py image_a image_b
"""


#!/usr/bin/env python
# import os
import sys
import numpy as np
# import imageio
from PIL import Image
# from PIL import ImageChops


def same(file_a, file_b, verbose=0):
    """ Determines if two images are the same or different.

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
        verbose: (Boolean): True provides more command line feedback that False.

    Returns:
        Boolean:  True for images are the same; False for images are different.
    """

    is_same = False

    try:
        im_a = Image.open(file_a)
    except IOError:
        print(f'Error: could not open file {file_a}.')

    try:
        im_b = Image.open(file_b)
    except IOError:
        print(f'Error: could not open file {file_b}.')

    im_a_size = im_a.size
    im_b_size = im_b.size

    if im_a_size == im_b_size:
        if verbose:
            print('Images are the same size.')

        data_a = np.array(im_a.getdata()).flatten()
        data_b = np.array(im_b.getdata()).flatten()
        data_diff = data_a - data_b
        data_diff_norm = np.linalg.norm(data_diff)
        image_tol = 1.0  # tolerance for the L2norm to be same or different

        if np.abs(data_diff_norm) > image_tol:
            if verbose:
                print('Images pixels are different.')
        else:
            if verbose:
                print('Images pixels are the same.')
            is_same = True

        # diff = ImageChops.difference(im_a, im_b)  # Chops is channel operations.

        # # Image.getbbox() gets the bounding box of all the non-zero regions in the image.
        # if diff.getbbox():
        #     if verbose:
        #         print('Images pixels are different.')
        # else:
        #     if verbose:
        #         print('Images pixels are the same.')
        #     is_same = True
    else:
        if verbose:
            print('Images are not the same size.')

    return is_same


def main(argv):
    """ The main entry point for command line interation.

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
        print(f'Error: {error}.')
        print('Abnormal script termination.')
        sys.exit('Two image files must be specified as arguments.')

    # if same(file_a, file_b, verbose=True):
    #     print('same method returned True.')
    # else:
    #     print('same method returned False.')
    same(file_a, file_b, verbose=True)


if __name__ == '__main__':
    main(sys.argv[1:])
