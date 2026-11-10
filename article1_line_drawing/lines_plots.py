"""Figure for article 1. Returns a matplotlib Figure; the caller shows or saves it.

No backend is forced here, so the figure also displays in Google Colab.
"""
import matplotlib.pyplot as plt

from lines import bresenham, rasterize, rasterize_wu, wu_line


def lines_figure():
    """Bresenham (stair-stepped) next to Wu (smooth) for the line (1,1) -> (10,6)."""
    hard = rasterize(bresenham(1, 1, 10, 6), (9, 12))
    soft = rasterize_wu(wu_line(1, 1, 10, 6), (9, 12))
    fig, ax = plt.subplots(1, 2, figsize=(9, 4))
    ax[0].imshow(hard, origin="lower", cmap="gray_r", vmin=0, vmax=1)
    ax[0].set_title("Bresenham (1,1) -> (10,6)")
    ax[1].imshow(soft, origin="lower", cmap="gray_r", vmin=0, vmax=1)
    ax[1].set_title("Wu (1,1) -> (10,6)")
    fig.tight_layout()
    return fig


FIGURES = {"lines_bresenham_vs_wu.png": lines_figure}
