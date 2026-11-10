import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")          # tests never open windows

# every article folder is self-contained: put each one on the import path
for folder in sorted(Path(__file__).parent.glob("article*")):
    sys.path.insert(0, str(folder))
