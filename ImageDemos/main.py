#!/usr/bin/env -S uv run --script
import random
from typing import Tuple

from image import Image, rgba


def rand_rgb():
    """
    Generates random RGB values for the RGBA class
    """
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return rgba(r, g, b)


def rand_pos(width: int, height: int) -> tuple[int, int]:
    """
    Generates a random position inside the image dimensions

    Args:
        width (int): the image width
        height (int): time image height
    """
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    return (x, y)


def create_image():
    """
    Creates an image with color pixels inside it
    """
    for frame in range(2):
        img = Image(512, 512)

        for y in range(img.width):
            for x in range(img.width):
                color = rand_rgb()
                img.set_pixel(x, y, color)

        img.save(f"test{frame:04}.png")


def create_line_image():
    """
    Creates an image full of horizontal, vertical and diagonal lines
    """
    width, height = 512, 512
    num_lines = 1000
    image = Image(width, height)

    for _ in range(num_lines):
        sx, sy = rand_pos(width, height)
        ex, ey = rand_pos(width, height)
        color = rand_rgb()
        image.line(sx, sy, ex, ey, color)

    image.save("lines_image.png")


def create_rectangle_image():
    width, height = 512, 512
    num_rects = 300
    img = Image(width, height)

    for _ in range(num_rects):
        (x1, y1) = rand_pos(width, height)
        (x2, y2) = rand_pos(width, height)

        img.rectangle(x1, y1, x2, y2, rand_rgb())

    img.save("rectangles_image.png")


def main():
    create_image()
    # create_line_image()
    # create_rectangle_image()


if __name__ == "__main__":
    main()
