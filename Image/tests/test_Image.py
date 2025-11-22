import pytest

from image import Image, ImageAccessError, rgba


@pytest.fixture
def red() -> rgba:
    return rgba(255, 0, 0)


def test_rgba_defaults():
    """
    Test that we default to black with full alpha
    """
    c = rgba()
    assert (c.r, c.g, c.b, c.a) == (0, 0, 0, 255)


def test_rgba_custom():
    """
    Test init from other values
    """
    c = rgba(255, 0, 128, 56)
    assert (c.r, c.g, c.b, c.a) == (255, 0, 128, 56)


def test_as_tuple(red):
    """
    Test the color vector as a tuple

    Args:
        red: numeric color value
    """
    assert red.as_tuple() == (255, 0, 0, 255)


@pytest.mark.parametrize(
    "component, value",
    [("r", -1), ("g", 256), ("b", 1000), ("a", -100), ("r", 25.0), ("b", "one")],
)
def test_invalid_values(component, value):
    """
    Test invalid rgba values

    Args:
        component: property key
        value: property value
    """
    with pytest.raises(ValueError):
        kwargs = {component: value}
        rgba(**kwargs)  # Double wildcard for programmatically print of the arguments


def test_default_image_ctor():
    """
    Test the default image constructor or init
    """
    img = Image(20, 10)
    assert img.width == 20
    assert img.height == 10


@pytest.fixture
def small_image() -> Image:
    return Image(10, 10)


@pytest.fixture
def red_image() -> Image:
    return Image(10, 10, rgba(255, 0, 0))


@pytest.fixture
def green_image() -> Image:
    return Image(10, 10, rgba(0, 255, 0))


@pytest.fixture
def blue_image() -> Image:
    return Image(10, 10, rgba(0, 0, 255))


def test_size_change_exception(small_image):
    """
    Test an image size change exception

    Args:
        small_image: image fixture
    """
    with pytest.raises(ImageAccessError):
        small_image.width = 100
    with pytest.raises(ImageAccessError):
        small_image.height = 100


def test_get_pixel(red_image, green_image, blue_image):
    """
    Test getting a pixel from an image

    Args:
        red_image: image all in red
        green_image: image all in green
        blue_image: image all in blue
    """
    for x in range(red_image.width):
        for y in range(red_image.height):
            r, g, b, a = red_image.get_pixel(x, y)
            assert r == 255
            assert g == 0
            assert b == 0
            assert a == 255

    for x in range(green_image.width):
        for y in range(green_image.height):
            r, g, b, a = green_image.get_pixel(x, y)
            assert r == 0
            assert g == 255
            assert b == 0
            assert a == 255

    for x in range(blue_image.width):
        for y in range(blue_image.height):
            r, g, b, a = blue_image.get_pixel(x, y)
            assert r == 0
            assert g == 0
            assert b == 255
            assert a == 255

    with pytest.raises(IndexError):
        red_image.get_pixel(200, 300)


def test_save():
    """
    Test saving an image
    """
    img = Image(1024, 1024)
    img.save("test.png")
    img = Image(1024, 1024, (255, 0, 0, 255))
    img.save("red.png")
    img = Image(1024, 1024, rgba(0, 255, 0, 255))
    img.save("green.png")


def test_set_pixel():
    """
    Test setting up a pixel inside an image
    """
    img = Image(3, 2)
    img.set_pixel(0, 0, rgba(255, 0, 0))
    img.set_pixel(1, 0, (0, 255, 0))
    img.set_pixel(2, 0, (0, 0, 255, 255))

    r, g, b, a = img.get_pixel(0, 0)
    assert (r, g, b, a) == (255, 0, 0, 255)
    r, g, b, a = img.get_pixel(1, 0)
    assert (r, g, b, a) == (0, 255, 0, 255)
    r, g, b, a = img.get_pixel(2, 0)
    assert (r, g, b, a) == (0, 0, 255, 255)

    img.set_pixel(0, 1, rgba(255, 0, 0, 128))
    img.set_pixel(1, 1, (0, 255, 0, 55))
    img.set_pixel(2, 1, (0, 0, 255, 205))

    r, g, b, a = img.get_pixel(0, 1)
    assert (r, g, b, a) == (255, 0, 0, 128)
    r, g, b, a = img.get_pixel(1, 1)
    assert (r, g, b, a) == (0, 255, 0, 55)
    r, g, b, a = img.get_pixel(2, 1)
    assert (r, g, b, a) == (0, 0, 255, 205)

    img.save("rgbatest.png")


def test_horizontal_line(small_image):
    """
    Test an horizontal line inside an image

    Args:
        small_image: image fixture
    """
    color = rgba(255, 0, 0, 255)
    small_image.line(2, 5, 7, 5, color)

    for x in range(2, 8):
        pixel = small_image.get_pixel(x, 5)
        assert tuple(int(c) for c in pixel) == color.as_tuple()


def test_vertical_line(small_image):
    """
    Test a vertical line inside an image

    Args:
        small_image: image fixture
    """
    color = rgba(0, 255, 0, 255)
    small_image.line(4, 2, 4, 7, color)

    for y in range(2, 8):
        pixel = small_image.get_pixel(4, y)
        assert tuple(int(c) for c in pixel) == color.as_tuple()


def test_diagonal_line(small_image):
    """
    Test a diagonal line inside an image

    Args:
        small_image: image fixture
    """
    color = rgba(0, 0, 255, 255)
    small_image.line(1, 1, 5, 5, color)

    for i in range(5):
        pixel = small_image.get_pixel(1 + i, 1 + i)
        assert tuple(int(c) for c in pixel) == color.as_tuple()


def test_rectangle_basic_fill():
    """
    Test the creation of a colored rectangle
    """
    img = Image(10, 10)
    color = rgba(255, 0, 0)

    img.rectangle(2, 3, 5, 6, color)

    for y in range(3, 7):
        for x in range(2, 6):
            assert tuple(img.get_pixel(x, y)) == color.as_tuple()
