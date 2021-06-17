# Stanford bunny

From 
https://graphics.stanford.edu/data/voldata/

```bash 
Description:    CT scan of the Stanford terra-cotta bunny
Dimensions:    360 slices of 512 x 512 pixels
               voxel grid is rectangular, and
               X:Y:Z aspect ratio of each voxel is 1:1:1
Files:         360 binary files, one file per slice
File format:    16-bit integers (Mac byte ordering), file contains no header
Data source:    Terry Yoo of the National Library of Medicine, using a scanner
               provided by Sandy Napel and Geoff Rubin of Stanford Radiology,
               of the terra-cotta bunny provided by Marc Levoy of Stanford CS
```

Files (slices) `1` to file `361` are all `524,288` bytes.  12-bit data stares as 16-bit (2 
byte) pixels, where 8 bits / byte = 16 bits (check).

Now, 512 x 512 pixels = 262,144 pixels per slice.  At 2 bytes per pixel, file size should be
524,288 byptes (check).

https://pypi.org/project/bitstring/ 

```bash
> cd ~/Downloads/bunny
> python
> myfile = open("99", "rb")
> data = myfile.read()
> len(data)
524288

>>> data[0:2]
b'\xf80'

>>> data[0:4]
b'\xf80\xf80'

>>> data[0:6]
b'\xf80\xf80\xf80'

>>> test = data[0:6]
>>> len(test)
6

from struct import *
fmt = 
pix = 
```
