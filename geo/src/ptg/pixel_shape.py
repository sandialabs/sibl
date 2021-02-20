from abc import ABC
from collections import namedtuple

import numpy as np


class PixelShapeBase(ABC):
    """Abstract base class for all 3D pixel shape classes.
    Creates a shape, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (k, j, i) voxel index, value at index is either:
        0 shape does not occupy that voxel,
        1 shape does occupy that voxel.
    k indexes `height`, j indexes `depth`, i indexes `width`.

    Arguments:
        width (float): width of shape in `len` units.  Defaults to 1.0 `len`.
        depth (float): depth of shape in `len` units.  Defaults to 1.0 `len`.
        height (float): height of shape in `len` units.  Defaults to 1.0 `len`.
        pixels_per_len (int): pixels per unit `len`.
            This is `pixel` resolution.  Increase `pixel_per_len` to increase resolution.
            Typical values include 150 pixels per inch and 300 pixels per inch.
            Defaults to 1 `pixel_per_len`.
        verbose (bool): True gives enhanced command line feedback.  Defaults to False.
        dtype (np.uint8): the data type of the pixel.

    Raises:
        ValueError: If `pixels_per_len` is less than 1.
        ValueError: If bounding box `width` or `depth` or `height` is less than 1.0.
    """

    def __init__(
        self,
        *,
        width: float = 1.0,
        depth: float = 1.0,
        height: float = 1.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):

        if pixels_per_len < 1:
            raise ValueError("Error: pixels_per_len (ppl) must be 1 'ppl' or greater.")

        if width < 1.0 or depth < 1.0 or height < 1.0:
            raise ValueError(
                "Error: width, depth, and height must be 1.0 'len' or greater."
            )

        if verbose:
            print("Creating object with following parameters:")
            print(f"bounding box width = {width} [len]")
            print(f"bounding box depth = {depth} [len]")
            print(f"bounding box height = {height} [len]")
            print(f"resolution = {pixels_per_len} [pixels per len]")
            print(f"data type = {dtype}")

        self._width_pixels = int(width * pixels_per_len)
        self._depth_pixels = int(depth * pixels_per_len)
        self._height_pixels = int(height * pixels_per_len)

        _bb = namedtuple("boundingbox", "width, depth, height")
        self._bounding_box = _bb(
            width=self._width_pixels,
            depth=self._depth_pixels,
            height=self._height_pixels,
        )
        self._mask = np.zeros(
            [self._width_pixels, self._depth_pixels, self._height_pixels], dtype=dtype
        )

    @property
    def bounding_box(self):
        """namedtuple("boundingbox", "width, depth, height"):
        Returns the shape's bounding box, in units of pixels, as a namedtuple, with
            width (int): width of shape in `pixel` units.
            depth (int): depth of shape in `pixel` units.
            height (int): height of shape in `pixel` units.
        """
        return self._bounding_box

    @property
    def mask(self):
        """np.array: Returns the 3D bit pixel mask as a numpy array, with (k, j, i)
        voxel index, value at index is either:
            0 cube does not occupy that voxel,
            1 cube does occupy that voxel (on boundary or interior).
        k indexes height, j indexes depth, i indexes width.
        """
        return self._mask


class PixelCube(PixelShapeBase):
    """Creates a cube, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (k, j, i) voxel index, value at index is either:
        0 cube does not occupy that voxel,
        1 cube does occupy that voxel (on boundary or interior).
    k indexes `height`, j indexes `depth`, i indexes `width`.

    Arguments:
        width (float): width of cube in `len` units.  Defaults to 1.0 `len`.
        pixels_per_len (int): pixels per unit `len`.
            This is `pixel` resolution.  Increase `pixel_per_len` to increase resolution.
            Typical values include 150 pixels per inch and 300 pixels per inch.
            Defaults to 1 `pixel_per_len`.
        verbose (bool): True gives enhanced command line feedback.  Defaults to False.
        dtype (np.uint8): the data type of the pixel.

    Raises:
        ValueError: If `pixels_per_len` is less than 1.
        ValueError: If bounding box `width` or `depth` or `height` is less than 1.0.
    """

    def __init__(
        self,
        *,
        width: float = 1.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):
        super().__init__(
            width=width,
            depth=width,
            height=width,
            pixels_per_len=pixels_per_len,
            verbose=verbose,
        )
        _width_pixels = int(width * pixels_per_len)

        self._mask = np.ones((_width_pixels, _width_pixels, _width_pixels), dtype=dtype)


class PixelSphere(PixelShapeBase):
    """Creates a sphere, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (k, j, i) voxel index, value at index is either:
        0 cube does not occupy that voxel,
        1 cube does occupy that voxel (on boundary or interior).
    k indexes `height`, j indexes `depth`, i indexes `width`.

    Arguments:
        radius (float): radius of sphere in `len` units.  Defaults to 1.0 `len`.
        pixels_per_len (int): pixels per unit `len`.
            This is `pixel` resolution.  Increase `pixel_per_len` to increase resolution.
            Typical values include 150 pixels per inch and 300 pixels per inch.
            Defaults to 1 `pixel_per_len`.
        verbose (bool): True gives enhanced command line feedback.  Defaults to False.
        dtype (np.uint8): the data type of the pixel.

    Raises:
        ValueError: If `pixels_per_len` is less than 1.
        ValueError: If bounding box `width` or `depth` or `height` is less than 1.0.
    """

    def __init__(
        self,
        *,
        radius: float = 1.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):
        super().__init__(
            width=2 * radius,
            depth=2 * radius,
            height=2 * radius,
            pixels_per_len=pixels_per_len,
            verbose=verbose,
            dtype=np.uint8,
        )

        _radius_pixels = int(radius * pixels_per_len)
        _diameter_pixels = int(2.0 * radius * pixels_per_len)

        self._mask = np.zeros(
            (_diameter_pixels, _diameter_pixels, _diameter_pixels), dtype=dtype
        )

        # For a sphere centered at (0, 0, 0), the surface
        # satisfies x^2 + y^2 + z^2 = R^2.  Here, the (0, 0, 0) points is
        # at the minimum coordinate of the bounding box.
        _radius_squared_pixels = int((radius * pixels_per_len) ** 2)

        for k in np.arange(_diameter_pixels):
            for j in np.arange(_diameter_pixels):
                for i in np.arange(_diameter_pixels):
                    # print(f"i: {i}, j:{j}, k:{k}")
                    voxel_center_squared = (
                        (i - _radius_pixels) ** 2
                        + (j - _radius_pixels) ** 2
                        + (k - _radius_pixels) ** 2
                    )
                    if voxel_center_squared <= _radius_squared_pixels:
                        self._mask[k, j, i] = 1


class PixelCylinder(PixelShapeBase):
    """Creates a cylinder, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (k, j, i) voxel index, value at index is either:
        0 cube does not occupy that voxel,
        1 cube does occupy that voxel (on boundary or interior).
    k indexes `height`, j indexes `depth`, i indexes `width`.

    Arguments:
        radius (float): radius of cylinder in `len` units.  Defaults to 1.0 `len`.
        height (float): height of cylinder in `len` units.  Defaults to 1.0 `len`.
        pixels_per_len (int): pixels per unit `len`.
            This is `pixel` resolution.  Increase `pixel_per_len` to increase resolution.
            Typical values include 150 pixels per inch and 300 pixels per inch.
            Defaults to 1 `pixel_per_len`.
        verbose (bool): True gives enhanced command line feedback.  Defaults to False.
        dtype (np.uint8): the data type of the pixel.

    Raises:
        ValueError: If `pixels_per_len` is less than 1.
        ValueError: If bounding box `width` or `depth` or `height` is less than 1.0.
    """

    def __init__(
        self,
        *,
        radius: float = 1.0,
        height: float = 1.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):
        super().__init__(
            width=2 * radius,
            depth=2 * radius,
            height=height,
            pixels_per_len=pixels_per_len,
            verbose=verbose,
            dtype=np.uint8,
        )

        _radius_pixels = int(radius * pixels_per_len)
        _diameter_pixels = int(2.0 * radius * pixels_per_len)
        _height_pixels = int(height * pixels_per_len)

        # perform radius calculations only once, on a single layer, then stack layers
        self._mask_layer = np.zeros((_diameter_pixels, _diameter_pixels), dtype=dtype)

        # For a cylinder centered at (0, 0, 0), the surface
        # satisfies x^2 + y^2 = R^2 for all z.
        _radius_squared_pixels = int((radius * pixels_per_len) ** 2)

        # one and only one computation, same for all layers, so only compute once
        for j in np.arange(_diameter_pixels):
            for i in np.arange(_diameter_pixels):
                print(f"i: {i}, j:{j}")
                voxel_center_squared = (i - _radius_pixels) ** 2 + (
                    j - _radius_pixels
                ) ** 2
                if voxel_center_squared <= _radius_squared_pixels:
                    self._mask_layer[j, i] = 1

        # stack z layers to assembly volume in z-direction
        self._mask = np.stack([self._mask_layer for _ in range(_height_pixels)])
