import sqlite3
from pathlib import Path
from typing import List

from lib.model.animalType import AnimalType
from lib.model.constants import RESERVES_ANIMALS_CLASSES
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.model.trophyanimal import TrophyAnimal


class TrophyAnimalManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self) -> None:
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

        conn.commit()
        conn.close()


    def insert_trophy_animals(self, trophy_animals: List[TrophyAnimal]) -> None:
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
        sql = trophyAnimalsSql

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

            sql = (f'WITH '
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