import sys
from pathlib import Path

from lib.db.db import Db
from lib.homePage import homePage
from lib.load.loader import Loader
from lib.ui.utils.paths import Paths

TEST_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
FIXTURES_PATH = TEST_DIR_PATH / 'fixtures'


def getDb() -> Db:
    db = Db(db_path=FIXTURES_PATH / 'data')
    db.load(Loader(paths=Paths(FIXTURES_PATH / 'trophy_lodges_adf')))
    return db


def getHomePage(paths: Paths):
    homePage(paths=paths, db_path=FIXTURES_PATH / 'data')
