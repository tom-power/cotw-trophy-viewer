import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import List

from lib.deca.hashes import hash32_func
from lib.load.loadTrophiesAnimals import loadTrophyAnimals
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
                int(animal.type),
                float(animal.weight) if animal.weight is not None else None,
                int(animal.gender) if animal.gender is not None else None,
                float(animal.rating) if animal.rating is not None else None,
                float(animal.medal) if animal.medal is not None else None,
                float(animal.difficulty) if animal.difficulty is not None else None,
                str(animal.datetime),
                int(animal.furType) if animal.furType is not None else None,
                int(animal.lodge) if animal.lodge is not None else None,
                int(animal.reserve) if animal.reserve is not None else None
            ))

        conn.commit()
        conn.close()

    def _insert_trophy_animals_reserves(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM AllAnimals')

        json_path = Path(__file__).parent.parent / 'config' / 'reserve_details.json'
        with open(json_path, 'r') as f:
            reserve_details = json.load(f)

        for reserve_key, reserve_data in reserve_details.items():
            reserve_index = reserve_data['index']
            species_list = reserve_data['species']

            for species in species_list:
                species_hash = hash32_func(species)
                cursor.execute('''
                    INSERT OR IGNORE INTO AllAnimals (reserve, type)
                    VALUES (?, ?)
                ''', (reserve_index, species_hash))

        conn.commit()
        conn.close()

    def trophyAnimals(self, query: dict = {}) -> List[TrophyAnimal]:
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

        if query != {}:
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

        if _lodgesIds:
            placeholders = ','.join(['?' for _ in _lodgesIds])
            where_clauses.append(f"lodge IN ({placeholders})")
            params.extend(_lodgesIds)

        if where_clauses and _reservesIds:
            where_clauses.append(f"{_reservesAndOr}")

        if _reservesIds:
            placeholders = ','.join(['?' for _ in _reservesIds])
            where_clauses.append(f"reserve IN ({placeholders})")
            params.extend(_reservesIds)

        if where_clauses and _medalsIds:
            where_clauses.append(f"{_medalsAndOr}")

        if _medalsIds:
            placeholders = ','.join(['?' for _ in _medalsIds])
            where_clauses.append(f"medal IN ({placeholders})")
            params.extend(_medalsIds)

        if where_clauses and _animalsIds:
            where_clauses.append(f"{_animalsAndOr}")

        if _animalsIds:
            placeholders = ','.join(['?' for _ in _animalsIds])
            where_clauses.append(f"type IN ({placeholders})")
            params.extend(_animalsIds)

        trophyAnimalsSql = """
        SELECT * FROM TrophyAnimals
        """
        if where_clauses:
            trophyAnimalsSql += " WHERE " + " ".join(where_clauses)
        sql=trophyAnimalsSql
        if _allAnimals:
            distinctTrophyAnimalsSql="""
            SELECT DISTINCT 
            type 
            FROM TrophyAnimals
            """
            allAnimalsSql = """
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

            sql=(f'WITH '
                 f'aa AS ({allAnimalsSql} WHERE type NOT IN ({distinctTrophyAnimalsSql})), '
                 f'ta AS ({trophyAnimalsSql}) '
                 f'SELECT * FROM ta '
                 f'UNION '
                 f'SELECT * FROM aa')

        cursor.execute(sql, params)
        rows = cursor.fetchall()

        trophy_animals = []
        for row in rows:
            animal = TrophyAnimal(
                animalType=int(row[1]) if row[1] is not None else None,
                weight=float(row[2]) if row[2] is not None else None,
                gender=int(row[3]) if row[3] is not None else None,
                rating=float(row[4]) if row[4] is not None else None,
                medal=float(row[5]) if row[5] is not None else None,
                difficulty=float(row[6]) if row[6] is not None else None,
                datetime=row[7],
                furType=int(row[8]) if row[8] is not None else None,
                lodge=int(row[9]) if row[9] is not None else None,
                reserve=int(row[10]) if row[10] is not None else None
            )
            animal.id = row[0]
            trophy_animals.append(animal)

        conn.close()
        return trophy_animals

    def lodges(self) -> dict:
        animals = sorted(self.trophyAnimals(), key=lambda x: x.lodge)
        lodges = list(map(lambda t: t.lodge, animals))
        return {l: f'LODGE {l}' for l in lodges}