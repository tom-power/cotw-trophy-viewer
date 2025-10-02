import sys
from pathlib import Path

if sys.platform == 'win32':
    DB_PATH = Path.home() / 'AppData' / 'Local' / 'cotw-trophy-viewer'
else:
    DB_PATH = Path.home() / '.cotw-trophy-viewer'