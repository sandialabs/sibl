from abc import ABC

import numpy as np


class PixelShapeBase(ABC):
    """Abstract base class for all ShapeDescendant classes"""

    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)


class PixelSphere(PixelShapeBase):
    """Create a sphere composed of pixels in R3"""

    def __init__(
        self,
        radius_len: float = 1.0,
        pixels_per_len: int = 2,
        position_x_len: int = 0,
        position_y_len: int = 0,
        position_z_len: int = 0,
        verbose: bool = False,
        **kwargs
    ):
        super().__init__(**kwargs)
        """Creates a sphere composed of a volume of stacked pixel images,
        encoded as a mask:
            0 outside of sphere,
            1 is on sphere boundary or interior
        """

        if radius_len < 1:
            raise ValueError("Error: radius must be 1 len or greater.")

        if pixels_per_len < 1:
            raise ValueError("Error: pixels_per_len (ppl) must be 1 ppl or greater.")

        radius = int(radius_len * pixels_per_len)  # pixels, radius, cast to int
        # diameter = 2 * radius
        n_sites_per_axis = int(2 * radius + 1)
        # hvsl = 0.5  # half of a a voxel side length

        # self._mask = np.zeros((diameter, diameter, diameter), dtype=int)
        self._mask = np.zeros(
            (n_sites_per_axis, n_sites_per_axis, n_sites_per_axis), dtype=int
        )

        # For a sphere centered at (0, 0, 0), the surface of the sphere
        # satisfies x^2 + y^2 + z^2 = R^2.
        radius_squared = radius ** 2

        for k in np.arange(n_sites_per_axis):
            for j in np.arange(n_sites_per_axis):
                for i in np.arange(n_sites_per_axis):
                    # print(f"i: {i}, j:{j}, k:{k}")
                    voxel_center_squared = (
                        (i - radius) ** 2 + (j - radius) ** 2 + (k - radius) ** 2
                    )
                    if voxel_center_squared <= radius_squared:
                        self._mask[k, j, i] = 1

    #         for k in np.arange(-radius, radius):
    #             for j in np.arange(-radius, radius):
    #                 for i in np.arange(-radius, radius):
    #                     # print(f"i: {i}, j:{j}, k:{k}")
    #                     voxel_center_squared = (
    #                         (i + hvsl) ** 2 + (j + hvsl) ** 2 + (k + hvsl) ** 2
    #                     )
    #                     if voxel_center_squared <= radius_squared:
    #                         self._mask[k + radius, j + radius, i + radius] = 1
    #
    @property
    def mask(self):
        """Returns the 3D bitmask as an numpy array, with  (k, j, i)
        voxel index, value at index is either:
            0 shape does not occupy that voxel,
            1 shape does occupy that voxel.
        """
        return self._mask
