from dataclasses import dataclass
from typing import Tuple, Union

import numpy as np
from PIL import Image as PILImage


@dataclass
class rgba:
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 255

    def as_tuple(self) -> tuple[int, int, int, int]:
        """Get the rgba as a tuple for easy access"""
        return (self.r, self.g, self.b, self.a)

    def __post_init__(self):
        for component in ("r", "g", "b", "a"):
            value = getattr(self, component)
            if not isinstance(value, int) or not (0 <= value <= 255):
                raise ValueError(
                    f"RGBA component {component} must be an int from 0 to 255"
                )


class ImageAccessError(Exception):
    """This Exception is thrown when trying to change size of Image"""

    pass


class Image:
    """
    A class that represents an image.
    """

    def __init__(
        self, width: int, height: int, fill_color: Union[rgba, tuple, None] = None
    ) -> None:
        """
        Initialize the Image.

        Args:
            width: The width of the image.
            height: The height of the image.
            fill_color: The color to fill the image with.
        """

        self._width = width
        self._height = height
        fill = self._validate_rgba(fill_color)

        # After completing the setup, create an rgba data
        self._rgba_data = np.full((self._height, self._width, 4), fill, dtype=np.uint8)

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value) -> None:
        raise ImageAccessError("Trying to set read only property width")

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value) -> None:
        raise ImageAccessError("Trying to set read only property height")

    def _validate_rgba(
        self, value: Union[rgba, tuple, None]
    ) -> Tuple[int, int, int, int]:
        """
        Check to see if a value is correct and return a tuple of RGBA values.

        Args:
            value: The value of the rgba check

        Returns:
            A tuple of RGBA values.
        """

        match value:
            case None:
                return (255, 255, 255, 255)
            case rgba(r, g, b, a):
                return (r, g, b, a)
            case (r, g, b):
                return (r, g, b, 255)
            case (r, g, b, a):
                return (r, g, b, a)
            case _:
                raise TypeError(f"Invalid type of RGBA color: {type(value).__name__}")

    def _check_bounds(self, x: int, y: int) -> None:
        """
        Check if the given x and y coordinates are within the bounds of the image.

        Args:
            x (int): The x coordinate to check.
            y (int): The y coordinate to check.

        Raises:

            : If the coordinates are out of the image.
        """

        if not (0 <= x <= self.width and 0 <= y <= self.height):
            raise IndexError(
                f"X or Y values out of range {x=} {self.width=} {y=} {self.height=}"
            )

    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int, int]:
        """
        Get the pixel from x and y, return as tuple

        Args:
            x (int): x cord of the pixel
            y (int): y cord of the pixel

        Returns current r, g, b, a of the pixel if range is valid
        """

        self._check_bounds(x, y)
        return tuple(self._rgba_data[y, x])

    def set_pixel(self, x: int, y: int, value: Union[tuple, rgba]) -> None:
        """
        Set the pixel at X and Y to the given value.

        Args:
            x (int): The X coordinate of the pixel.
            y (int): The Y coordinate of the pixel.
           value: The value to set the pixel to.
        """

        self._check_bounds(x, y)
        self._rgba_data[y, x] = self._validate_rgba(value)

    def save(self, name: str) -> None:
        """
        Save the image to a file.

        Args:
            name: The name of the file to save the image to.
        """

        img = PILImage.fromarray(self._rgba_data)
        img.save(name)

    def clear(self, color):
        """
        Clears the color within the rgba data

        Args:
            color: the color value
        """
        self._rgba_data[:] = color

    def line(self, sx: int, sy: int, ex: int, ey: int, color: rgba) -> None:
        """
        This method draws a line based on specific vectors or parameters.

        Args:
            tx (int): Initial X coordinate of the line.
            ty (int): Initial Y coordinate of the line.
            bx (int): Final X coordinate of the line.
            by (int): Final Y coordinate of the line.
            color (Union[tuple, rgba]): Color of the line.
        """

        line_color = self._validate_rgba(color)

        dx = abs(sx - ex)
        dy = abs(sy - ey)
        sx_step = 1 if sx < ex else -1
        sy_step = 1 if sy < ey else -1

        # Set default X and Y values
        x, y = sx, sy
        deviation = 0

        if dx > dy:
            deviation = dx // 2

            for _ in range(dx + 1):
                try:
                    self.set_pixel(x, y, line_color)
                except IndexError:
                    raise IndexError(f"Pixel ({x=}, {y=}) is out of bounds!") from None

                x += sx_step
                deviation -= dy

                # Everytime we move a pixel we adjust the deviation
                if deviation < 0:
                    y += sy_step
                    deviation += dx
        else:
            deviation = dy // 2

            for _ in range(dy + 1):
                try:
                    self.set_pixel(x, y, line_color)
                except IndexError:
                    raise IndexError(f"Pixel ({x=}, {y=}) is out of bounds!") from None

                y += sy_step
                deviation -= dx

                # Everytime we move a pixel we adjust the deviation
                if deviation < 0:
                    x += sx_step
                    deviation += dy

    def rectangle(self, tx: int, ty: int, bx: int, by: int, color: rgba) -> None:
        """
        Draw a rectangle.

        Args:
            tx (int): top-left x
            ty (int): top-left y
            bx (int): bottom-right x
            by (int): bottom-right y
            color (rgba): fill color
        """

        fill = self._validate_rgba(color)

        x1, x2 = sorted((tx, bx))
        y1, y2 = sorted((ty, by))

        # Clip to image bounds
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(self.width - 1, x2)
        y2 = min(self.height - 1, y2)

        if x1 > x2 or y1 > y2:
            return

        self._rgba_data[y1 : y2 + 1, x1 : x2 + 1] = fill
