# import numpy as np
import matplotlib.pyplot as plt

# from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from skimage.morphology import disk, ball
from skimage.draw import ellipsoid
from skimage import measure

# https://scikit-image.org/docs/stable/auto_examples/numpy_operations/plot_structuring_elements.html#sphx-glr-download-auto-examples-numpy-operations-plot-structuring-elements-py

# fig = plt.figure(figsize=(12, 4))
fig = plt.figure(figsize=(8, 8))
# create a disk 2D
# ax = fig.add_subplot(1, 3, 1)
ax = fig.add_subplot(111)
d = disk(4)
ax.imshow(d, cmap="Paired", vmin=0, vmax=12)
for i in range(d.shape[0]):
    for j in range(d.shape[1]):
        ax.text(j, i, d[i, j], ha="center", va="center", color="white")
fig.tight_layout()
plt.show()

# create a ball 3D
fig = plt.figure(figsize=(8, 8))
# ax = fig.add_subplot(1, 3, 2, projection="3d")
ax = fig.add_subplot(111, projection="3d")
b = ball(4)
ax.voxels(b)
dmax = 10
ax.set_xlim(0, dmax)
ax.set_ylim(0, dmax)
ax.set_zlim(0, dmax)
fig.tight_layout()
plt.show()

# create ellipsoid ball
fig = plt.figure(figsize=(8, 8))
# ax = fig.add_subplot(1, 3, 3, projection="3d")
ax = fig.add_subplot(111, projection="3d")
ell = ellipsoid(4, 4, 4, levelset=True)

# Marching cubes to create data for surface mesh
verts, faces, normals, values = measure.marching_cubes(ell, 0)

# fancy indexing: `verts[faces]` to create set of triangles
mesh = Poly3DCollection(verts[faces])
mesh.set_edgecolor("black")
ax.add_collection3d(mesh)

ax.set_xlim(0, dmax)
ax.set_ylim(0, dmax)
ax.set_zlim(0, dmax)

fig.tight_layout()
plt.show()


# References:
# Smooth Voxel Terrain (Part 2)
# https://0fps.net/2012/07/12/smooth-voxel-terrain-part-2/
# Marching Cubes (MC), Marching Tetrahedra (MT), Surface Nets (SN)
# https://github.com/mikolalysenko/mikolalysenko.github.com/blob/master/Isosurface/js/surfacenets.js

# https://graphics.stanford.edu/~mdfisher/MarchingCubes.html

# Isosurface Polygonization
# http://www2.compute.dtu.dk/~janba/gallery/polygonization.html
# Dual contouring was originally called Surface Nets by Sarah Frisken
# T. Ju, F. Losasso, S. Schaefer, and J. Warren.  (2004)  “Dual Contouring of Hermite Data”  SIGGRAPH 2004


# https://stackoverflow.com/questions/6030098/how-to-display-a-3d-plot-of-a-3d-array-isosurface-in-matplotlib-mplot3d-or-simil

# https://stackoverflow.com/questions/6485908/basic-dual-contouring-theory
# https://web.archive.org/web/20170713094715if_/http://www.frankpetterson.com/publications/dualcontour/dualcontour.pdf

# Patient-specific vascular NURBS modeling for isogeometric analysis of blood flow
# Y Zhang, Y Bazilevs, S Goswami, CL Bajaj, TJR Hughes
# Computer methods in applied mechanics and engineering 196 (29-30), 2943-2959	429
# "There are two main isocontouring methods from imaging data: Primal Contouring (or Marching Cubes [37]) and Dual Contouring [38]. In this application we choose Dual Contouring to extract the isosurface, because it tends to generate meshes with better aspect ratios. We then modify the model to suit our particular application. This can be done in various ways, for example, by removing unnecessary components, adding necessary components which are not constructed from imaging data, denoising the surface, etc. After getting the vessel path, we can edit it according to simulation requirements."


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
