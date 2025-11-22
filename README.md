# Image Drawing Library

This project implements a simple image drawing engine in Python. It supports:

- Creating images by pixels
- Drawing lines (Bresenham algorithm)
- Drawing rectangles with clipping
- Saving images to PNG

The repository also contains demo functions that generate colorful images illustrating how the system works.

---

```mermaid
classDiagram
    %% Core classes
    class rgba {
        int r
        int g
        int b
        int a
        __post_init__()
        tuple as_tuple()
    }

    class Image {
        - int _width
        - int _height
        - ndarray _rgba_data
        + int width
        + int height
        + __init__(width, height, fill_color)
        + _validate_rgba(value)
        + _check_bounds(x, y)
        + get_pixel(x, y)
        + set_pixel(x, y, value)
        + clear(color)
        + save(name)
        + line(sx, sy, ex, ey, color)
        + rectangle(tx, ty, bx, by, color)
    }

    %% Demo functions / ImageDemos
    class ImageDemos {
        + rand_rgb() : rgba
        + rand_pos(width, height) : tuple[int,int]
        + create_image()
        + create_line_image()
        + create_rectangle_image()
        + main()
    }

    %% Relationships
    Image --> rgba : uses
    ImageDemos --> Image : creates/uses
    ImageDemos --> rgba : uses
```

---

# Demos

This section describes each demo function and provides space for example images.

---

## `create_image()`

**Description:**
Fills the entire image with random colors on a per-pixel basis. Useful for testing basic pixel manipulation and color rendering.

**Example Output:**

![Pixel Image](/Users/fhidalgo/Documents/BU/image-demo/ImageDemos/test0000.png)

---

## `create_line_image()`

**Description:**
Draws multiple lines (horizontal, vertical, diagonal) at random positions and in random colors. Demonstrates the `Image.line()` method using Bresenham’s algorithm.

**Example Output:**

![Line Image](/Users/fhidalgo/Documents/BU/image-demo/ImageDemos/lines_image.png)

---

## `create_rectangle_image()`

**Description:**
Draws multiple rectangles at random positions with random fill colors. Demonstrates the `Image.rectangle()` method with automatic clipping to the image bounds.

**Example Output:**

![Rectangle Image](/Users/fhidalgo/Documents/BU/image-demo/ImageDemos/rectangles_image.png)
