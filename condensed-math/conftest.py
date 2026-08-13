"""Let the tests import the build scripts that sit next to this file."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
