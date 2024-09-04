import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import the modules
from toolkit import *
from jobs import *
from config import *
from extensions import *
from scripts import *

# Clean up sys.path
sys.path.pop(0)

# If you want to define __all__ to control what's imported with "from ostris_ai_toolkit import *"
__all__ = ['toolkit', 'jobs', 'config', 'extensions', 'scripts']