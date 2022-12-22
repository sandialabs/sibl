# Copyright 2020 National Technology and Engineering Solutions of Sandia, LLC (NTESS).
# Under the terms of Contract DE-NA0003525 with NTESS, the U.S. Government retains
# certain rights in this software.


from abc import ABC

# from collections import namedtuple
from typing import NamedTuple

import numpy as np


class PixelAnchor(NamedTuple):
    """Create the shape's anchor (x, y, z) position, in units of pixels, as a
    namedtuple, with the following attributes:

    Attributes:
        x (int): x-coordinate of position in `pixel` units.  Defaults to 0.
        y (int): y-coordinate of position in `pixel` units.  Defaults to 0.
        x (int): z-coordinate of position in `pixel` units.  Defaults to 0.
    """

    x: int = 0  # pixels
    y: int = 0  # pixels
    z: int = 0  # pixels


class PixelBoundingBox(NamedTuple):
    """Creates the shape's bounding box, in units of pixels, as a namedtuple, with
    the following attributes:

    Attributes:
        dx (int): height of shape in `pixel` units. Defaults to 1.
        dy (int): depth of shape in `pixel` units. Defaults to 1.
        dz (int): width of shape in `pixel` units. Defaults to 1.
    """

    dx: int = 1  # pixels
    dy: int = 1  # pixels
    dz: int = 1  # pixels


class PixelShapeBase(ABC):
    """Abstract base class for all 3D pixel shape classes.
    Creates a shape, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (i, j, k) voxel index, value at index is either:
        0 shape does not occupy that voxel,
        1 shape does occupy that voxel.
    i indexes `height`, j indexes `depth`, k indexes `width`.

    Keyword Arguments:
        anchor_x (float): x-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_y (float): y-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_z (float): z-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        dx (float): height of shape in `len` units.  Defaults to 1.0 `len`.
        dy (float): depth of shape in `len` units.  Defaults to 1.0 `len`.
        dz (float): width of shape in `len` units.  Defaults to 1.0 `len`.
        pixels_per_len (int): pixels per unit `len`.
            This is `pixel` resolution.  Increase `pixel_per_len` to increase resolution.
            Typical values include 150 pixels per inch and 300 pixels per inch.
            Defaults to 1 `pixel_per_len`.
        verbose (bool): True gives enhanced command line feedback.  Defaults to False.
        dtype (np.uint8): the data type of the pixel.

    Raises:
        ValueError: If `pixels_per_len` < 1.
        ValueError: If bounding box `dx` or `dy` or `dz` < 1.0.
    """

    def __init__(
        self,
        *,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        anchor_z: float = 0.0,
        dx: float = 1.0,
        dy: float = 1.0,
        dz: float = 1.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):

        if pixels_per_len < 1:
            raise ValueError("Error: pixels_per_len (ppl) must be 1 'ppl' or greater.")

        if dx < 1.0 or dy < 1.0 or dz < 1.0:
            raise ValueError("Error: dx, dy, and dz must be 1.0 'len' or greater.")

        if verbose:
            print("Creating object with following parameters:")
            print(f"bounding box dx = {dx} [len]")
            print(f"bounding box dy = {dy} [len]")
            print(f"bounding box dz = {dz} [len]")
            print(f"resolution = {pixels_per_len} [pixels per len]")
            print(f"data type = {dtype}")

        self._anchor_x_pixels = int(anchor_x * pixels_per_len)
        self._anchor_y_pixels = int(anchor_y * pixels_per_len)
        self._anchor_z_pixels = int(anchor_z * pixels_per_len)

        self._dx_pixels = int(dx * pixels_per_len)
        self._dy_pixels = int(dy * pixels_per_len)
        self._dz_pixels = int(dz * pixels_per_len)

        self._mask = np.zeros(
            [self._dx_pixels, self._dy_pixels, self._dz_pixels], dtype=dtype
        )

    @property
    def anchor(self) -> PixelAnchor:
        """PixelAnchor"""
        return PixelAnchor(
            x=self._anchor_x_pixels, y=self._anchor_y_pixels, z=self._anchor_z_pixels
        )

    @property
    def bounding_box(self) -> PixelBoundingBox:
        """PixelBoundingBox"""
        return PixelBoundingBox(
            dx=self._dx_pixels, dy=self._dy_pixels, dz=self._dz_pixels
        )

    @property
    def mask(self) -> np.ndarray:
        """np.ndarray: Returns the 3D bit pixel mask as a numpy array, with (i, j, k)
        voxel index, value at index is either:
            0 (int) cube does not occupy that voxel,
            1 (int) cube does occupy that voxel (on boundary or interior).
        i indexes height, j indexes depth, k indexes width.
        """
        return self._mask


class PixelCube(PixelShapeBase):
    """Creates a cube, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (i, j, k) voxel index, value at index is either:
        0 shape does not occupy that voxel,
        1 shape does occupy that voxel.
    i indexes `height`, j indexes `depth`, k indexes `width`.

    Keyword Arguments:
        anchor_x (float): x-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_y (float): y-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_z (float): z-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        dx (float): height of shape in `len` units.  Defaults to 1.0 `len`.
        pixels_per_len (int): pixels per unit `len`.
            This is `pixel` resolution.  Increase `pixel_per_len` to increase resolution.
            Typical values include 150 pixels per inch and 300 pixels per inch.
            Defaults to 1 `pixel_per_len`.
        verbose (bool): True gives enhanced command line feedback.  Defaults to False.
        dtype (np.uint8): the data type of the pixel.

    Raises:
        ValueError: If `pixels_per_len` < 1.
        ValueError: If bounding box `dx` or `dy` or `dz` < 1.0.
    """

    def __init__(
        self,
        *,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        anchor_z: float = 0.0,
        dx: float = 1.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):
        super().__init__(
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            anchor_z=anchor_z,
            dx=dx,
            dy=dx,
            dz=dx,
            pixels_per_len=pixels_per_len,
            verbose=verbose,
        )
        _dx_pixels = int(dx * pixels_per_len)

        self._mask = np.ones((_dx_pixels, _dx_pixels, _dx_pixels), dtype=dtype)


class PixelCylinder(PixelShapeBase):
    """Creates a cylinder, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (i, j, k) voxel index, value at index is either:
        0 shape does not occupy that voxel,
        1 shape does occupy that voxel.
    i indexes `height`, j indexes `depth`, k indexes `width`.

    Keyword Arguments:
        anchor_x (float): x-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_y (float): y-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_z (float): z-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        height (float): height of cylinder in `len` units, in `dx` dimension.
            Defaults to 1.0 `len`.
        diameter_inner (float): inner diameter (>=0) of cylinder in `len` units.
            If zero, the shape is solid.  If greater than zero, the shape is hallow.
            Defaults to 2.0 `len`.
        diameter_outer (float): outer diameter of cylinder in `len` units (diameter = dy = dz).
            Defaults to 4.0 `len`.
        pixels_per_len (int): pixels per unit `len`.
            This is `pixel` resolution.  Increase `pixel_per_len` to increase resolution.
            Typical values include 150 pixels per inch and 300 pixels per inch.
            Defaults to 1 `pixel_per_len`.
        verbose (bool): True gives enhanced command line feedback.  Defaults to False.
        dtype (np.uint8): the data type of the pixel.

    Raises:
        ValueError: If `diameter_inner` < 0 or `diameter_inner` >= `diameter_outer`.
        ValueError: If `pixels_per_len` < 1.
        ValueError: If bounding box `dx` or `dy` or `dz` < 1.0.
    """

    def __init__(
        self,
        *,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        anchor_z: float = 0.0,
        height: float = 1.0,
        diameter_inner: float = 2.0,
        diameter_outer: float = 4.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):
        super().__init__(
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            anchor_z=anchor_z,
            dx=height,
            dy=diameter_outer,
            dz=diameter_outer,
            pixels_per_len=pixels_per_len,
            verbose=verbose,
            dtype=np.uint8,
        )

        if diameter_inner < 0.0:
            raise ValueError("Error: diameter_inner must be >= 0.0.")

        if diameter_inner >= diameter_outer:
            raise ValueError("Error: diameter_inner must be < diameter_outer.")

        # _radius_pixels = int(diameter_outer / 2.0 * pixels_per_len) + 1
        _radius_inner_pixels = int(diameter_inner / 2.0 * pixels_per_len)
        _radius_outer_pixels = int(diameter_outer / 2.0 * pixels_per_len) + 1
        # _radius_outer_pixels = int(diameter_outer / 2.0 * pixels_per_len)
        _diameter_outer_pixels = int(diameter_outer * pixels_per_len)
        _height_pixels = int(height * pixels_per_len)

        _y, _z = np.mgrid[
            -_radius_outer_pixels : _radius_outer_pixels : _diameter_outer_pixels * 1j,
            -_radius_outer_pixels : _radius_outer_pixels : _diameter_outer_pixels * 1j,
        ]
        _r_squared = _y**2 + _z**2

        _b0 = 1  # pixels, allow for edge case with outside diameter

        # inner radius test must be <= to avoid holes in filled cylinders when
        # outer diameter is an odd number
        _inner_mask = np.array(
            _radius_inner_pixels * _radius_inner_pixels <= _r_squared
        )
        _outer_mask = np.array(
            _r_squared <= _radius_outer_pixels * _radius_outer_pixels + _b0 * _b0
        )

        # now intersection of inner radius mask and outer radius mask
        self._mask_layer = np.array(_inner_mask * _outer_mask, dtype=dtype)

        # stack x layers to assembly volume in x-direction
        self._mask = np.stack([self._mask_layer for _ in range(_height_pixels)])


class PixelQuarterCylinder(PixelShapeBase):
    """Creates a quarter cylinder, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (i, j, k) voxel index, value at index is either:
        0 shape does not occupy that voxel,
        1 shape does occupy that voxel.
    i indexes `height`, j indexes `depth`, k indexes `width`.

    Keyword Arguments:
        anchor_x (float): x-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_y (float): y-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_z (float): z-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        height (float): height of cylinder in `len` units, in `dx` dimension.
            Defaults to 1.0 `len`.
        radius_inner (float): inner radius (>=0) of cylinder in `len` units.
            If zero, the is shape is solid.  If greater than zero, the shape hollow.
            Defaults to 1.0 `len`.
        radius_outer (float): outer radius of cylinder in `len` units.
            Defaults to 2.0 `len`.
        pixels_per_len (int): pixels per unit `len`.
            This is `pixel` resolution.  Increase `pixel_per_len` to increase resolution.
            Typical values include 150 pixels per inch and 300 pixels per inch.
            Defaults to 1 `pixel_per_len`.
        verbose (bool): True gives enhanced command line feedback.  Defaults to False.
        dtype (np.uint8): the data type of the pixel.

    Raises:
        ValueError: If `radius_inner` < 0 or `radius_inner` >= `radius_outer`.
        ValueError: If `pixels_per_len` < 1.
        ValueError: If bounding box `dx` or `dy` or `dz` < 1.0.
    """

    def __init__(
        self,
        *,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        anchor_z: float = 0.0,
        height: float = 1.0,
        radius_inner: float = 1.0,
        radius_outer: float = 2.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):
        super().__init__(
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            anchor_z=anchor_z,
            dx=height,
            dy=radius_outer,
            dz=radius_outer,
            pixels_per_len=pixels_per_len,
            verbose=verbose,
            dtype=np.uint8,
        )

        if radius_inner < 0.0:
            raise ValueError("Error: radius_inner must be >= 0.0.")

        if radius_inner >= radius_outer:
            raise ValueError("Error: radius_inner must be < radius_outer.")

        _radius_inner_pixels = int(radius_inner * pixels_per_len)
        _radius_outer_pixels = int(radius_outer * pixels_per_len)
        _height_pixels = int(height * pixels_per_len)

        _y, _z = np.mgrid[
            1 : _radius_outer_pixels + 1,
            1 : _radius_outer_pixels + 1,
        ]
        _r_squared = _y**2 + _z**2

        # accommodate radius, r, measurement as r^2 = a^2 + b^2, where
        # a = radius, in pixels, defined by user input, and
        # b = 1 pixel, because on the y-axis and z-axis, the minimum
        #   perpendicular length is 1 pixel (not zero pixels).
        _ai = _radius_inner_pixels
        _ao = _radius_outer_pixels
        _b = 1  # pixels

        _inner_mask = np.array((_ai * _ai) + (_b * _b) < _r_squared)
        _outer_mask = np.array(_r_squared <= (_ao * _ao) + (_b * _b))

        # now intersection of inner radius mask and outer radius mask
        self._mask_layer = np.array(_inner_mask * _outer_mask, dtype=dtype)

        # stack x layers to assembly volume in x-direction
        self._mask = np.stack([self._mask_layer for _ in range(_height_pixels)])


class PixelSphere(PixelShapeBase):
    """Creates a sphere, at `pixel_per_len` resolution, composed of pixels as
    the 3D bit mask numpy array, with (i, j, k) voxel index, value at index is either:
        0 shape does not occupy that voxel,
        1 shape does occupy that voxel.
    i indexes `height`, j indexes `depth`, k indexes `width`.

    Keyword Arguments:
        anchor_x (float): x-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_y (float): y-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        anchor_z (float): z-position in `len` units of shape's anchor (0, 0, 0)
            in world coordinate system.  Defaults to 0.0 `len`.
        diameter (float): diameter of sphere in `len` units (diameter = dx = dy = dz).
            Defaults to 2.0 `len`.
        pixels_per_len (int): pixels per unit `len`.
            This is `pixel` resolution.  Increase `pixel_per_len` to increase resolution.
            Typical values include 150 pixels per inch and 300 pixels per inch.
            Defaults to 1 `pixel_per_len`.
        verbose (bool): True gives enhanced command line feedback.  Defaults to False.
        dtype (np.uint8): the data type of the pixel.

    Raises:
        ValueError: If `pixels_per_len` < 1.
        ValueError: If bounding box `dx` or `dy` or `dz` < 1.0.
    """

    def __init__(
        self,
        *,
        anchor_x: float = 0.0,
        anchor_y: float = 0.0,
        anchor_z: float = 0.0,
        diameter: float = 2.0,
        pixels_per_len: int = 1,
        verbose: bool = False,
        dtype=np.uint8,
    ):
        super().__init__(
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            anchor_z=anchor_z,
            dx=diameter,
            dy=diameter,
            dz=diameter,
            pixels_per_len=pixels_per_len,
            verbose=verbose,
            dtype=np.uint8,
        )

        _radius_pixels = int(diameter / 2.0 * pixels_per_len) + 1
        _diameter_pixels = int(diameter * pixels_per_len)

        _x, _y, _z = np.mgrid[
            -_radius_pixels : _radius_pixels : _diameter_pixels * 1j,
            -_radius_pixels : _radius_pixels : _diameter_pixels * 1j,
            -_radius_pixels : _radius_pixels : _diameter_pixels * 1j,
        ]

        _r_squared = _x**2 + _y**2 + _z**2
        self._mask = np.array(
            _r_squared <= _radius_pixels * _radius_pixels, dtype=dtype
        )


class BoundingBoxLines:
    """Creates collection of points to compose lines of a shape's bounding box.

    Arguments:
        shape (PixelShapeBase): the shape object.
    """

    def __init__(self, shape: PixelShapeBase) -> None:

        _x0, _y0, _z0 = shape.anchor.x, shape.anchor.y, shape.anchor.z
        _dx, _dy, _dz = (
            shape.bounding_box.dx,
            shape.bounding_box.dy,
            shape.bounding_box.dz,
        )
        _x1, _y1, _z1 = _x0 + _dx, _y0 + _dy, _z0 + _dz

        self._edges_dx = np.array(
            [
                [[_x0, _y0, _z0], [_x1, _y0, _z0]],
                [[_x0, _y0, _z1], [_x1, _y0, _z1]],
                [[_x0, _y1, _z0], [_x1, _y1, _z0]],
                [[_x0, _y1, _z1], [_x1, _y1, _z1]],
            ],
        )

        self._edges_dy = np.array(
            [
                [[_x0, _y0, _z0], [_x0, _y1, _z0]],
                [[_x0, _y0, _z1], [_x0, _y1, _z1]],
                [[_x1, _y0, _z0], [_x1, _y1, _z0]],
                [[_x1, _y0, _z1], [_x1, _y1, _z1]],
            ],
        )

        self._edges_dz = np.array(
            [
                [[_x0, _y0, _z0], [_x0, _y0, _z1]],
                [[_x0, _y1, _z0], [_x0, _y1, _z1]],
                [[_x1, _y0, _z0], [_x1, _y0, _z1]],
                [[_x1, _y1, _z0], [_x1, _y1, _z1]],
            ],
        )

    @property
    def edges_dx(self) -> np.ndarray:
        """np.ndarray: Returns a numpy array of point pairs, (x, y, z) in pixel units,
        composing edges of the bounding box parallel with the x direction."""
        return self._edges_dx

    @property
    def edges_dy(self) -> np.ndarray:
        """np.ndarray: Returns a numpy array of point pairs, (x, y, z) in pixel units,
        composing edges of the bounding box parallel with the y direction."""
        return self._edges_dy

    @property
    def edges_dz(self) -> np.ndarray:
        """np.ndarray: Returns a numpy array of point pairs, (x, y, z) in pixel units,
        composing edges of the bounding box parallel with the z direction."""
        return self._edges_dz
