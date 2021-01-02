import numpy as np

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
