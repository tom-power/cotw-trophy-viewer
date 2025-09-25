import os
import sqlite3
import sys
from pathlib import Path

from lib.load.loadTrophiesAnimals import loadTrophyAnimals
from .preset_manager import PresetManager
from .trophy_animal_manager import TrophyAnimalManager

TEST_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
DB_PATH = Path('data')

class Db:
    def __init__(self, loadPath: Path, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path / "trophy_viewer.db"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._create_database()
        self.trophy_animal_manager = TrophyAnimalManager(self.db_path)
        self.trophy_animal_manager.insert_trophy_animals(loadTrophyAnimals(loadPath))
        self.trophy_animal_manager.insert_trophy_animals_reserves()
        self.preset_manager = PresetManager(self.db_path)
        self.preset_manager.presetInit()

    def _create_database(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TrophyAnimals (
                id TEXT PRIMARY KEY,
                type INTEGER,
                weight REAL,
                gender INTEGER,
                rating REAL,
                medal REAL,
                difficulty REAL,
                datetime TEXT,
                furType INTEGER,
                lodge INTEGER,
                reserve INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS AllAnimals (
                reserve INTEGER,
                type INTEGER,
                PRIMARY KEY (reserve, type)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Preset (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                query TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()



    def trophyAnimals(self, query: dict | None = None):
        return self.trophy_animal_manager.trophyAnimals(query)

    def lodges(self) -> dict:
        return self.trophy_animal_manager.lodges()

    def presets(self):
        return self.preset_manager.presets()

    def preset(self, i: int) -> dict:
        return self.preset_manager.preset(i)

    def presetsClear(self):
        return self.preset_manager.presetsClear()

    def presetInit(self):
        return self.preset_manager.presetInit()

    def presetAdd(self, name, queryDict):
        return self.preset_manager.presetAdd(name, queryDict)

    def presetRemove(self, presetId):
        return self.preset_manager.presetRemove(presetId)