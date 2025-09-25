import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import List

from lib.load.loadTrophiesAnimals import loadTrophyAnimals
from lib.model.animalType import AnimalType
from lib.model.constants import RESERVES_ANIMALS_CLASSES
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.model.trophyanimal import TrophyAnimal

TEST_DIR_PATH = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
DB_PATH = Path('data')

class Db:
    def __init__(self, loadPath: Path, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path / "trophy_viewer.db"
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._create_database()
        self._insert_trophy_animals(loadTrophyAnimals(loadPath))
        self._insert_trophy_animals_reserves()
        self._insert_default_presets()

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

    def _insert_trophy_animals(self, trophy_animals: List[TrophyAnimal]) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM TrophyAnimals')

        for animal in trophy_animals:
            cursor.execute('''
                INSERT INTO TrophyAnimals
                (id, type, weight, gender, rating, medal, difficulty, datetime, furType, lodge, reserve)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(animal.id),
                int(animal.type.value) if animal.type is not None else None,
                float(animal.weight) if animal.weight is not None else None,
                int(animal.gender) if animal.gender is not None else None,
                float(animal.rating) if animal.rating is not None else None,
                int(animal.medal.value) if animal.medal is not None else None,
                float(animal.difficulty) if animal.difficulty is not None else None,
                str(animal.datetime),
                int(animal.furType) if animal.furType is not None else None,
                int(animal.lodge) if animal.lodge is not None else None,
                int(animal.reserve.value) if animal.reserve is not None else None
            ))

        conn.commit()
        conn.close()

    def _insert_trophy_animals_reserves(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM AllAnimals')

        for reserve_enum, reserve_dict in RESERVES_ANIMALS_CLASSES.items():
            reserve_index = reserve_enum.value

            for class_level, animals_list in reserve_dict.items():
                for animal_type in animals_list:
                    cursor.execute('''
                        INSERT OR IGNORE INTO AllAnimals (reserve, type)
                        VALUES (?, ?)
                    ''', (reserve_index, animal_type.value))

        conn.commit()
        conn.close()

    def _insert_default_presets(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM Preset')
        if cursor.fetchone()[0] == 0:
            default_preset_query = {
                "lodges": [],
                "reserves": [],
                "medals": [0],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

            cursor.execute(
                'INSERT INTO Preset (name, query) VALUES (?, ?)',
                ('diamond checklist', json.dumps(default_preset_query))
            )

        conn.commit()
        conn.close()

    def trophyAnimals(self, query: dict | None = None) -> List[TrophyAnimal]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        _lodgesIds = []
        _reservesAndOr = ''
        _reservesIds = []
        _medalsAndOr = ''
        _medalsIds = []
        _animalsAndOr = ''
        _animalsIds = []
        _allAnimals = False

        if query is not None:
            _lodgesIds = query.get('lodges', [])
            _reservesAndOr = query.get('reservesAndOr', '')
            _reservesIds = query.get('reserves', [])
            _medalsAndOr = query.get('medalsAndOr', '')
            _medalsIds = query.get('medals', [])
            _animalsAndOr = query.get('animalsAndOr', '')
            _animalsIds = query.get('animals', [])
            _allAnimals = query.get('allAnimals', False)

        where_clauses = []
        params = []
        trophyParams = []

        if _lodgesIds:
            reservePlaceholders = ','.join(['?' for _ in _lodgesIds])
            where_clauses.append(f"lodge IN ({reservePlaceholders})")
            trophyParams.extend(_lodgesIds)

        if where_clauses and _reservesIds:
            where_clauses.append(f"{_reservesAndOr}")

        if _reservesIds:
            reservePlaceholders = ','.join(['?' for _ in _reservesIds])
            where_clauses.append(f"reserve IN ({reservePlaceholders})")
            trophyParams.extend(_reservesIds)

        if where_clauses and _medalsIds:
            where_clauses.append(f"{_medalsAndOr}")

        if _medalsIds:
            reservePlaceholders = ','.join(['?' for _ in _medalsIds])
            where_clauses.append(f"medal IN ({reservePlaceholders})")
            trophyParams.extend(_medalsIds)

        if where_clauses and _animalsIds:
            where_clauses.append(f"{_animalsAndOr}")

        if _animalsIds:
            reservePlaceholders = ','.join(['?' for _ in _animalsIds])
            where_clauses.append(f"type IN ({reservePlaceholders})")
            trophyParams.extend(_animalsIds)


        trophyAnimalsSql = """
        SELECT * FROM TrophyAnimals
        """
        if where_clauses:
            trophyAnimalsSql += " WHERE " + " ".join(where_clauses)

        params = trophyParams
        sql=trophyAnimalsSql

        if _allAnimals:
            allAnimalsParams = []

            trophyTypesSubquery = f"SELECT DISTINCT type FROM ({trophyAnimalsSql})"

            allAnimalsSelectSql = """
                SELECT DISTINCT
                NULL as id,
                type,
                NULL as weight,
                NULL as gender,
                NULL as rating,
                NULL as medal,
                NULL as difficulty,
                NULL as datetime,
                NULL as furType,
                NULL as lodge,
                NULL as reserve
                FROM AllAnimals
                """

            allAnimalsSql = (allAnimalsSelectSql
                             + f""" WHERE type NOT IN ({trophyTypesSubquery})""")

            if _reservesIds:
                reservePlaceholders = ','.join(['?' for _ in _reservesIds])
                allAnimalsSql = (allAnimalsSelectSql
                                 + f""" WHERE type NOT IN ({trophyTypesSubquery}) AND reserve IN ({reservePlaceholders}) """)
                allAnimalsParams.extend(_reservesIds)

            sql=(f'WITH '
                 f'ta AS ({trophyAnimalsSql}), '
                 f'aa AS ({allAnimalsSql}) '
                 f'SELECT * FROM ta '
                 f'UNION '
                 f'SELECT * FROM aa')

            params = trophyParams + trophyParams + allAnimalsParams

        cursor.execute(sql, params)
        rows = cursor.fetchall()

        trophy_animals = []
        for row in rows:
            animal = TrophyAnimal(
                animalType=AnimalType(int(row[1])) if row[1] is not None else None,
                weight=float(row[2]) if row[2] is not None else None,
                gender=int(row[3]) if row[3] is not None else None,
                rating=float(row[4]) if row[4] is not None else None,
                medal=Medal(int(row[5])) if row[5] is not None else None,
                difficulty=float(row[6]) if row[6] is not None else None,
                datetime=row[7],
                furType=int(row[8]) if row[8] is not None else None,
                lodge=int(row[9]) if row[9] is not None else None,
                reserve=Reserve(int(row[10])) if row[10] is not None else None
            )
            animal.id = row[0]
            trophy_animals.append(animal)

        conn.close()
        return trophy_animals

    def lodges(self) -> dict:
        animals = sorted(self.trophyAnimals(), key=lambda x: x.lodge)
        lodges = list(map(lambda t: t.lodge, animals))
        return {l: f'LODGE {l}' for l in lodges}

    def presets(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT id, name FROM Preset ORDER BY id')
        rows = cursor.fetchall()

        conn.close()
        return {row[0]: row[1] for row in rows}

    def preset(self, i: int) -> dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT query FROM Preset WHERE id = ?', (i,))
        row = cursor.fetchone()

        conn.close()
        if row:
            return json.loads(row[0])
        else:
            return {}

    def presetsClear(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            'DELETE FROM Preset'
        )

        conn.commit()
        conn.close()

    def presetInit(self):
        self._insert_default_presets()

    def presetAdd(self, name, queryDict):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            'INSERT OR IGNORE INTO Preset (name, query) VALUES (?, ?)',
            (name, json.dumps(queryDict))
        )

        conn.commit()
        conn.close()

    def presetRemove(self, presetId):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            'DELETE FROM Preset WHERE id = ?',
            (presetId,)
        )

        conn.commit()
        conn.close()