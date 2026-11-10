import random

import numpy as np
import pytest

from lines import bresenham, dda, rasterize, rasterize_wu, wu_line


def ideal_minor_axis_error(pts, x0, y0, x1, y1):
    """Largest distance (along the minor axis) between pixels and the ideal line."""
    worst = 0.0
    for x, y in pts:
        if abs(x1 - x0) >= abs(y1 - y0):
            ideal = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
            worst = max(worst, abs(y - ideal))
        else:
            ideal = x0 + (x1 - x0) * (y - y0) / (y1 - y0)
            worst = max(worst, abs(x - ideal))
    return worst


def random_lines(n=300, seed=1):
    rng = random.Random(seed)
    for _ in range(n):
        x0, y0, x1, y1 = (rng.randint(-30, 30) for _ in range(4))
        if (x0, y0) != (x1, y1):
            yield x0, y0, x1, y1


def test_bresenham_article_example():
    assert bresenham(1, 1, 8, 6) == [(1, 1), (2, 2), (3, 2), (4, 3),
                                     (5, 4), (6, 5), (7, 5), (8, 6)]


def test_bresenham_all_octants_hit_endpoints_and_length():
    for x0, y0, x1, y1 in random_lines():
        pts = bresenham(x0, y0, x1, y1)
        assert pts[0] == (x0, y0) and pts[-1] == (x1, y1)
        assert len(pts) == max(abs(x1 - x0), abs(y1 - y0)) + 1


def test_bresenham_stays_within_half_pixel_of_ideal_line():
    for line in random_lines():
        assert ideal_minor_axis_error(bresenham(*line), *line) <= 0.5 + 1e-9


def test_bresenham_uses_only_integers():
    assert all(isinstance(v, int) for p in bresenham(0, 0, 13, 5) for v in p)


def test_dda_article_example_matches_bresenham():
    assert dda(1, 1, 8, 6) == bresenham(1, 1, 8, 6)


def test_dda_all_octants_hit_endpoints_and_length():
    for x0, y0, x1, y1 in random_lines():
        pts = dda(x0, y0, x1, y1)
        assert pts[0] == (x0, y0) and pts[-1] == (x1, y1)
        assert len(pts) == max(abs(x1 - x0), abs(y1 - y0)) + 1


def test_dda_stays_within_half_pixel_for_short_lines():
    for line in random_lines():
        assert ideal_minor_axis_error(dda(*line), *line) <= 0.5 + 1e-9


def test_dda_single_point():
    assert dda(3, 4, 3, 4) == [(3, 4)]


def test_float32_increments_accumulate_error():
    """The weakness DDA has and Bresenham does not: repeated float additions drift."""
    step, n = np.float32(0.1), 100_000
    total = np.float32(0.0)
    for _ in range(n):
        total += step
    assert abs(float(total) - n * 0.1) > 1.0


def test_wu_example_values():
    samples = [(x, y, round(a, 2)) for x, y, a in wu_line(1, 1, 10, 6)[:6]]
    assert samples == [(1, 1, 1.0), (1, 2, 0.0), (2, 1, 0.44),
                       (2, 2, 0.56), (3, 2, 0.89), (3, 3, 0.11)]


def test_wu_intensities_sum_to_one_and_reproduce_the_line():
    x0, y0, x1, y1 = 1, 1, 10, 6
    samples = wu_line(x0, y0, x1, y1)
    for k in range(0, len(samples), 2):
        (x, ylow, a_low), (_, yhigh, a_high) = samples[k], samples[k + 1]
        assert a_low + a_high == pytest.approx(1.0)
        assert 0 <= a_low <= 1 and 0 <= a_high <= 1
        weighted_y = ylow * a_low + yhigh * a_high
        assert weighted_y == pytest.approx(y0 + (y1 - y0) * (x - x0) / (x1 - x0))


def test_wu_rejects_unsupported_lines():
    with pytest.raises(ValueError):
        wu_line(5, 1, 1, 3)       # x0 >= x1
    with pytest.raises(ValueError):
        wu_line(1, 1, 3, 9)       # slope above 1


def test_rasterize_shapes():
    assert rasterize(bresenham(1, 1, 8, 6), (8, 10)).sum() == 8
    img = rasterize_wu(wu_line(1, 1, 10, 6), (9, 12))
    assert img.shape == (9, 12) and img.max() == 1.0


def test_lines_figure_returns_a_figure():
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure

    from lines_plots import lines_figure

    fig = lines_figure()
    assert isinstance(fig, Figure)
    plt.close(fig)
