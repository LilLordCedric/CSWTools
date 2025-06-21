import sys
import os
from pathlib import Path

# Add the parent directory to sys.path to allow importing the package
sys.path.insert(0, str(Path(__file__).parent.parent))