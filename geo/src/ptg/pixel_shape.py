from abc import ABC
from collections import namedtuple
from typing import NamedTuple

import numpy as np


class PixelShapeBase(ABC):
    """Abstract base class for all 3D pixel shape classes.
    Creates a shape, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (k, j, i) voxel index, value at index is either:
        0 shape does not occupy that voxel,
        1 shape does occupy that voxel.
    k indexes `height`, j indexes `depth`, i indexes `width`.

    Keyword Arguments:
        anchor_x (float): x-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_y (float): y-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_z (float): z-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
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
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        anchor_z: float = 0.0,
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

        _bb = namedtuple("boundingbox", ["width", "depth", "height"])
        self._bounding_box = _bb(
            width=self._width_pixels,
            depth=self._depth_pixels,
            height=self._height_pixels,
        )
        self._mask = np.zeros(
            [self._width_pixels, self._depth_pixels, self._height_pixels], dtype=dtype
        )

        _anchor = namedtuple("anchor", ["x", "y", "z"])
        self._anchor = _anchor(
            x=int(anchor_x * pixels_per_len),
            y=int(anchor_y * pixels_per_len),
            z=int(anchor_z * pixels_per_len),
        )

    @property
    def bounding_box(self) -> NamedTuple:
        """NamedTuple: namedtuple("boundingbox", ["width", "depth", "height"]):
        Returns the shape's bounding box, in units of pixels, as a namedtuple, with
            width (int): width of shape in `pixel` units.
            depth (int): depth of shape in `pixel` units.
            height (int): height of shape in `pixel` units.
        """
        return self._bounding_box

    @property
    def mask(self) -> np.ndarray:
        """np.ndarray: Returns the 3D bit pixel mask as a numpy array, with (k, j, i)
        voxel index, value at index is either:
            0 cube does not occupy that voxel,
            1 cube does occupy that voxel (on boundary or interior).
        k indexes height, j indexes depth, i indexes width.
        """
        return self._mask

    @property
    def anchor(self) -> NamedTuple:
        """NamedTuple: namedtuple("anchor", ["x", "y", "z"]):
        Returns the shape's anchor point coordinates, in units of pixels,
        as a namedtuple, with
            x (int): x-position of shape's anchor point in `pixel` units.
            y (int): y-position of shape's anchor point in `pixel` units.
            z (int): z-position of shape's anchor point in `pixel` units.
        """
        return self._anchor


class PixelCube(PixelShapeBase):
    """Creates a cube, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (k, j, i) voxel index, value at index is either:
        0 cube does not occupy that voxel,
        1 cube does occupy that voxel (on boundary or interior).
    k indexes `height`, j indexes `depth`, i indexes `width`.

    Keyword Arguments:
        anchor_x (float): x-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_y (float): y-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_z (float): z-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
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
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        anchor_z: float = 0.0,
        width: float = 1.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):
        super().__init__(
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            anchor_z=anchor_z,
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

    Keyword Arguments:
        anchor_x (float): x-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_y (float): y-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_z (float): z-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
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
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        anchor_z: float = 0.0,
        radius: float = 1.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):
        super().__init__(
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            anchor_z=anchor_z,
            width=2 * radius,
            depth=2 * radius,
            height=2 * radius,
            pixels_per_len=pixels_per_len,
            verbose=verbose,
            dtype=np.uint8,
        )

        _radius_pixels = int(radius * pixels_per_len)

        _diameter_pixels = 2 * _radius_pixels + 1
        _z, _y, _x = np.mgrid[
            -_radius_pixels : _radius_pixels : _diameter_pixels * 1j,
            -_radius_pixels : _radius_pixels : _diameter_pixels * 1j,
            -_radius_pixels : _radius_pixels : _diameter_pixels * 1j,
        ]

        _r_squared = _x ** 2 + _y ** 2 + _z ** 2
        self._mask = np.array(
            _r_squared <= _radius_pixels * _radius_pixels, dtype=dtype
        )


class PixelCylinder(PixelShapeBase):
    """Creates a cylinder, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (k, j, i) voxel index, value at index is either:
        0 cube does not occupy that voxel,
        1 cube does occupy that voxel (on boundary or interior).
    k indexes `height`, j indexes `depth`, i indexes `width`.

    Keyword Arguments:
        anchor_x (float): x-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_y (float): y-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_z (float): z-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
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
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        anchor_z: float = 0.0,
        radius: float = 1.0,
        height: float = 1.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):
        super().__init__(
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            anchor_z=anchor_z,
            width=2 * radius,
            depth=2 * radius,
            height=height,
            pixels_per_len=pixels_per_len,
            verbose=verbose,
            dtype=np.uint8,
        )

        _radius_pixels = int(radius * pixels_per_len)
        _height_pixels = int(height * pixels_per_len)

        _diameter_pixels = 2 * _radius_pixels + 1
        _y, _x = np.mgrid[
            -_radius_pixels : _radius_pixels : _diameter_pixels * 1j,
            -_radius_pixels : _radius_pixels : _diameter_pixels * 1j,
        ]

        _r_squared = _x ** 2 + _y ** 2
        self._mask_layer = np.array(
            _r_squared <= _radius_pixels * _radius_pixels, dtype=dtype
        )

        # stack z layers to assembly volume in z-direction
        self._mask = np.stack([self._mask_layer for _ in range(_height_pixels)])
