"""Generate the figures of every article into <article>/figures.

Each article has a `*_plots.py` module with a FIGURES dict: file name -> function
that returns a matplotlib Figure. Every article folder that exists is processed.

    python scripts/make_figures.py [--article article1_line_drawing]
"""
import argparse
import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")          # only for this script: write files, never open a window
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def load_plots(plots_file):
    """Import a *_plots.py file with its own folder on sys.path (it imports its sibling module)."""
    import sys
    sys.path.insert(0, str(plots_file.parent))
    spec = importlib.util.spec_from_file_location(plots_file.stem, plots_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--article", help="process only this article folder")
    args = parser.parse_args()
    for folder in sorted(ROOT.glob("article*")):
        if args.article and folder.name != args.article:
            continue
        for plots_file in sorted(folder.glob("*_plots.py")):
            plots = load_plots(plots_file)
            out_dir = folder / "figures"
            out_dir.mkdir(exist_ok=True)
            for name, make in plots.FIGURES.items():
                fig = make()
                fig.savefig(out_dir / name, dpi=150)
                plt.close(fig)
                print("wrote", f"{folder.name}/figures/{name}")
