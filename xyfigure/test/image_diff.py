#!/usr/bin/env python
import os
import sys
import numpy as np
# import imageio
from PIL import Image, ImageChops

def same(file_a, file_b, verbose=0):

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

        diff = ImageChops.difference(im_a, im_b)  # Chops is channel operations.

        # Image.getbbox() gets the bounding box of all the non-zero regions in the image.
        if diff.getbbox():
            if verbose:
                print('Images pixels are different.')
        else:
            if verbose: 
                print('Images pixels are the same.')
            is_same = True
    else:
        if verbose:
            print('Images are not the same size.')

    return is_same


def main(argv):

    try:
        file_a = argv[0]
        file_b = argv[1]
    except IndexError as error:
        print(f'Error: {error}.')
        print('Abnormal script termination.')
        sys.exit('Two image files must be specified as arguments.')

    if same(file_a, file_b, verbose=True):
        print('same method returned True.')
    else:
        print('same method returned False.')

if __name__ == '__main__':
    main(sys.argv[1:])
