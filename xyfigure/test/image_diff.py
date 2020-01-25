#!/usr/bin/env python
import os
import sys
import numpy as np
# import imageio
from PIL import Image, ImageChops

def main(argv):

    try:
        file_a = argv[0]
        file_b = argv[1]
    except IndexError as error:
        print(f'Error: {error}.')
        print('Abnormal script termination.')
        sys.exit('Two image files must be specified as arguments.')

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
        print('Images are the same size.')
        diff = ImageChops.difference(im_a, im_b)
        # Image.getbbox() gets the bounding box of all the non-zero regions in the image.
        if diff.getbbox():
            print('Images pixels are different.')
        else:
            print('Images pixels are the same.')
    else:
        print('Images are not the same size.')

if __name__ == '__main__':
    main(sys.argv[1:])
