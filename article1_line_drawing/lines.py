"""Line drawing on a pixel grid: DDA, Bresenham and Wu's anti-aliased line.

Article 1: Bresenham's algorithm and anti-aliasing.
"""
import math

import numpy as np


def dda(x0, y0, x1, y1):
    """DDA: step one pixel along the longer axis, add a float increment to the other.

    Needs one floating-point addition per step, so rounding error accumulates
    with the length of the line.
    """
    n = max(abs(x1 - x0), abs(y1 - y0))      # steps along the longer axis
    if n == 0:
        return [(x0, y0)]
    dx, dy = (x1 - x0) / n, (y1 - y0) / n    # one of them is +1 or -1
    x, y, pts = float(x0), float(y0), []
    for _ in range(n + 1):
        pts.append((math.floor(x + 0.5), math.floor(y + 0.5)))
        x += dx
        y += dy
    return pts


def bresenham(x0, y0, x1, y1):
    """Bresenham's line for all eight octants, using integer arithmetic only."""
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if (x0, y0) == (x1, y1):
            break
        e2 = 2 * err        # doubling removes the 0.5 fraction; still exact
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
    return pts


def wu_line(x0, y0, x1, y1):
    """Wu-style anti-aliased line as (x, y, intensity) samples.

    Simplified: requires x0 < x1 and a slope between 0 and 1, and does not treat
    the end points separately or apply gamma correction.
    """
    if not x0 < x1:
        raise ValueError("wu_line needs x0 < x1")
    m = (y1 - y0) / (x1 - x0)
    if not 0 <= m <= 1:
        raise ValueError("wu_line needs a slope between 0 and 1")
    out, y = [], float(y0)
    for x in range(x0, x1 + 1):
        yi = math.floor(y)
        f = y - yi                      # fractional part
        out.append((x, yi,     1 - f))  # lower pixel
        out.append((x, yi + 1, f))      # upper pixel
        y += m
    return out


def rasterize(points, shape):
    """Binary image from a list of (x, y) pixels. Row index is y."""
    grid = np.zeros(shape)
    for x, y in points:
        grid[y, x] = 1
    return grid


def rasterize_wu(samples, shape):
    """Grey-level image from Wu samples (keeps the brighter value per pixel)."""
    img = np.zeros(shape)
    for x, y, a in samples:
        img[y, x] = max(img[y, x], a)
    return img
