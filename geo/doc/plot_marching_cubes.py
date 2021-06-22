import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from skimage import measure
from skimage.draw import ellipsoid


def vertex_int_filter(x: np.ndarray) -> bool:
    # if x[0] % 1 == 0 and x[1] % 1 == 0 and x[2] % 1 == 0:
    #     return True
    # else:
    #     return False

    t = tuple(map(lambda y: y % 1 == 0, x))
    return all(t)


# Generate a level set about zero of two identical ellipsoids in 3D
a, b, c = 2, 2, 2
ellip_base = ellipsoid(a, b, c, levelset=True)
# ellip_double = np.concatenate((ellip_base[:-1, ...], ellip_base[2:, ...]), axis=0)

# Use marching cubes to obtain the surface mesh of these ellipsoids
# verts, faces, normals, values = measure.marching_cubes(ellip_double, 0)
verts, faces, normals, values = measure.marching_cubes(ellip_base, 0)

# verts_on_lattice = tuple(filter(vertex_int_filter, verts))
verts_on_lattice = np.squeeze(tuple(filter(vertex_int_filter, verts)))
xs, ys, zs = verts_on_lattice[:, 0], verts_on_lattice[:, 1], verts_on_lattice[:, 2]

# Display resulting triangular mesh using Matplotlib. This can also be done
# with mayavi (see skimage.measure.marching_cubes_lewiner docstring).
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")

# Fancy indexing: `verts[faces]` to generate a collection of triangles
mesh = Poly3DCollection(verts[faces])
mesh.set_edgecolor("k")
ax.add_collection3d(mesh)
ax.scatter(xs, ys, zs, color="red", marker="o")

ax.set_xlabel(f"x-axis: a = {a} per ellipsoid")
ax.set_ylabel(f"y-axis: b = {b}")
ax.set_zlabel(f"z-axis: c = {c}")

ax.set_xlim(0, 2 * a)  # a = 6 (times two for 2nd ellipsoid)
ax.set_ylim(0, 2 * b)  # b = 10
ax.set_zlim(0, 2 * c)  # c = 16

plt.tight_layout()
plt.show()
