"""Put the topic folder on the import path so tests can import the builders.

`tests/test_guide.py` imports `build_guide` to check that the generated chapter
files still match ARTICLE.md.  Pytest puts the tests folder on the path, not the
folder above it, so this does that one job.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
