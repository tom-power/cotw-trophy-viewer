import sys
from pathlib import Path

TEST_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
FIXTURES_PATH = TEST_DIR_PATH / 'fixtures'

def mapAnimalTypes(trophyAnimalType: str) -> str:
    match trophyAnimalType:
        case '1511159411':
            return "FALLOW DEER"
        case _:
            return trophyAnimalType
