"""Build the notebooks: one local and one Google Colab version per article.

Each article folder has a `notebook_cells.py` with its cells. Every article folder
that exists is built, so a new article only needs its own folder.

Both versions share the same body cells; only the first (setup) cell and the
Colab badge differ. The local notebook is executed so the saved outputs show up
on GitHub, and the same outputs are copied into the Colab version.

    python scripts/make_notebooks.py [--repo OWNER/NAME] [--article article1_line_drawing]

Needs: pip install -r requirements-dev.txt
"""
import argparse
import importlib.util
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))   # for notebook_tools

from notebook_tools import COLAB_SETUP, LOCAL_SETUP  # noqa: E402

DEFAULT_REPO = "AliGaderian/Computer_Graphics_LinkedIn_Group"


def load_cells(article_dir):
    spec = importlib.util.spec_from_file_location(
        f"{article_dir.name}_cells", article_dir / "notebook_cells.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def to_cells(items):
    return [new_markdown_cell(text) if kind == "md" else new_code_cell(text)
            for kind, text in items]


def build(article_dir, repo):
    cells = load_cells(article_dir)
    article = article_dir.name
    repo_name = repo.split("/")[-1]       # `git clone` creates a folder with this name
    meta = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"}}

    # local version: execute it, so outputs are stored in the file
    setup = new_code_cell(LOCAL_SETUP.format(module=cells.MODULE).strip("\n"))
    local = new_notebook(cells=[setup] + to_cells(cells.ITEMS), metadata=dict(meta))
    local_dir = article_dir / "local"
    local_dir.mkdir(parents=True, exist_ok=True)
    NotebookClient(local, timeout=300, kernel_name="python3",
                   resources={"metadata": {"path": str(local_dir)}}).execute()
    nbformat.validate(local)
    nbformat.write(local, local_dir / f"{cells.FILE_NAME}.ipynb")

    # colab version: same body cells (and outputs), different setup cell + badge
    badge_url = (f"https://colab.research.google.com/github/{repo}/blob/main/"
                 f"{article}/colab/{cells.FILE_NAME}.ipynb")
    badge = new_markdown_cell(
        f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({badge_url})")
    colab_setup = new_code_cell(
        COLAB_SETUP.format(repo=repo, name=repo_name, article=article).strip("\n"))
    colab = new_notebook(cells=[badge, colab_setup] + local.cells[1:], metadata=dict(meta))
    colab_dir = article_dir / "colab"
    colab_dir.mkdir(parents=True, exist_ok=True)
    nbformat.validate(colab)
    nbformat.write(colab, colab_dir / f"{cells.FILE_NAME}.ipynb")
    print("wrote", article)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=DEFAULT_REPO,
                        help="GitHub owner/name used in the Colab links")
    parser.add_argument("--article", help="build only this article folder")
    args = parser.parse_args()
    folders = sorted(p for p in ROOT.glob("article*") if (p / "notebook_cells.py").exists())
    for folder in folders:
        if args.article is None or folder.name == args.article:
            build(folder, args.repo)
