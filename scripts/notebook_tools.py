"""Helpers shared by scripts/make_notebooks.py and the articles' notebook_cells.py."""


def rtl(text):
    """Wrap Persian markdown so it renders right-to-left."""
    return f'<div dir="rtl">\n\n{text.strip()}\n\n</div>'


def md(text):
    return ("md", rtl(text))


def code(text):
    return ("code", text.strip("\n"))


LOCAL_SETUP = '''
# Local run: make this article's code importable (finds the folder that contains {module}.py).
import pathlib
import sys

root = pathlib.Path.cwd()
while not (root / "{module}.py").exists() and root != root.parent:
    root = root.parent
sys.path.insert(0, str(root))
'''

COLAB_SETUP = '''
# Google Colab: fetch the repository once, then import this article's code from it.
# NumPy and matplotlib are already installed in Colab, so nothing is reinstalled.
import os
import subprocess
import sys

REPO_URL = "https://github.com/{repo}.git"
if not os.path.exists("{name}"):
    subprocess.run(["git", "clone", "-q", REPO_URL], check=True)
os.chdir("{name}/{article}")
sys.path.insert(0, os.getcwd())
'''
