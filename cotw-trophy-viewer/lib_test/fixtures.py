import sys
from pathlib import Path

TEST_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
FIXTURES_PATH = TEST_DIR_PATH / 'fixtures'