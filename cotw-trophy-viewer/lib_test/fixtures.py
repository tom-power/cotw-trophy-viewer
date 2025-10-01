import sys
from pathlib import Path

from lib.db.db import Db
from lib.load.loader import Loader

TEST_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
FIXTURES_PATH = TEST_DIR_PATH / 'fixtures'


def getDb() -> Db:
    db = Db(db_path=FIXTURES_PATH / 'data')
    db.load(Loader(loadPath=FIXTURES_PATH))
    return db
