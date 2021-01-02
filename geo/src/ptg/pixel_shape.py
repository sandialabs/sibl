from abc import ABC

import numpy as np


class PixelShapeBase(ABC):
    """Abstract base class for all ShapeDescendant classes"""

    def __init__(
        self,
        width_len: float = 1.0,
        depth_len: float = 1.0,
        height_len: float = 1.0,
        pixels_per_len: int = 2,
        verbose: bool = False,
        **kwargs,
    ):
        self.id = kwargs.get("id", None)
        self._mask = None

        if pixels_per_len < 1:
            raise ValueError("Error: pixels_per_len (ppl) must be 1 ppl or greater.")
        if width_len < 1 or depth_len < 1:
            raise ValueError("Error: width and depth must be 1 len or greater.")
        if height_len < 1:
            raise ValueError("Error: height must be 1 len or greater.")

    @property
    def mask(self):
        """Returns the 3D bit mask as an numpy array, with  (k, j, i)
        voxel index, value at index is either:
            0 shape does not occupy that voxel,
            1 shape does occupy that voxel.
            k indexes height, j indexes depth, i indexes width.
        """
        return self._mask


class PixelSphere(PixelShapeBase):
    """Create a sphere composed of pixels in R3"""

    def __init__(
        self,
        radius_len: float = 1.0,
        pixels_per_len: int = 2,
        verbose: bool = False,
        **kwargs,
    ):
        super().__init__(
            width_len=2 * radius_len,
            depth_len=2 * radius_len,
            height_len=2 * radius_len,
            pixels_per_len=pixels_per_len,
            verbose=verbose,
            **kwargs,
        )
        """Creates a sphere composed of a volume of stacked pixel images,
        encoded as a mask:
            0 outside of sphere,
            1 is on sphere boundary or interior
        """

        # no longer needed since base class checks minimum bounding box dimensions
        # if radius_len < 1:
        #     raise ValueError("Error: radius must be 1 len or greater.")

        radius = int(radius_len * pixels_per_len)  # pixels, radius, cast to int
        n_sites_per_axis = int(2 * radius + 1)

        self._mask = np.zeros(
            (n_sites_per_axis, n_sites_per_axis, n_sites_per_axis), dtype=int
        )

        # For a sphere centered at (0, 0, 0), the surface
        # satisfies x^2 + y^2 + z^2 = R^2.  Here, the (0, 0, 0) points is
        # at the minimum coordinate of the bounding box.
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


class PixelCylinder(PixelShapeBase):
    """Create a right circular cylinder composed of pixels in R3"""

    def __init__(
        self,
        radius_len: float = 1.0,
        height_len: float = 1.0,
        pixels_per_len: int = 2,
        verbose: bool = False,
        **kwargs,
    ):
        super().__init__(
            width_len=2 * radius_len,
            depth_len=2 * radius_len,
            height_len=height_len,
            pixels_per_len=pixels_per_len,
            verbose=verbose,
            **kwargs,
        )
        """Creates a cylinder composed of a volume of stacked pixel images,
        encoded as a mask:
            0 outside of cylinder,
            1 is on cylinder boundary or interior
        """

        # no longer needed since base class checks minimum bounding box dimensions
        # if radius_len < 1:
        #     raise ValueError("Error: radius must be 1 len or greater.")

        radius = int(radius_len * pixels_per_len)  # pixels, radius, cast to int
        n_sites_per_axis = int(2 * radius + 1)

        height = int(height_len * pixels_per_len)  # pixels, height, cast to int
        n_sites_per_axis_z = int(height + 1)

        self._mask_layer = np.zeros((n_sites_per_axis, n_sites_per_axis), dtype=int)

        # For a cylinder centered at (0, 0, 0), the surface
        # satisfies x^2 + y^2 = R^2 for all z.
        radius_squared = radius ** 2

        # one and only one computation, same for all layers, so only compute once
        for j in np.arange(n_sites_per_axis):
            for i in np.arange(n_sites_per_axis):
                print(f"i: {i}, j:{j}")
                voxel_center_squared = (i - radius) ** 2 + (j - radius) ** 2
                if voxel_center_squared <= radius_squared:
                    self._mask_layer[j, i] = 1

        # stack z layers to assembly volume in z-direction
        self._mask = np.stack([self._mask_layer for _ in range(n_sites_per_axis_z)])
