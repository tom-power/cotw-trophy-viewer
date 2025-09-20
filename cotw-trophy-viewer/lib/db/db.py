import sqlite3
from pathlib import Path
from typing import List
import os

from lib.load.loadTrophiesAnimals import loadTrophyAnimals
from lib.model.trophyanimal import TrophyAnimal

DB_PATH = 'cotw-trophy-viewer/lib/db/data/'

class Db:
    def __init__(self, loadPath: Path, db_path: str = DB_PATH + "trophy_viewer.db") -> None:
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._create_database()
        self._insert_trophy_animals(loadTrophyAnimals(loadPath))

    def _create_database(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TrophyAnimals (
                id TEXT PRIMARY KEY,
                type TEXT,
                weight REAL,
                gender INTEGER,
                score REAL,
                rating REAL,
                badge INTEGER,
                difficulty REAL,
                datetime TEXT,
                furType INTEGER,
                lodge INTEGER,
                reserve INTEGER
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
                (id, type, weight, gender, score, rating, badge, difficulty, datetime, furType, lodge, reserve)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                str(animal.id),
                int(animal.type),
                float(animal.weight) if animal.weight is not None else None,
                int(animal.gender) if animal.gender is not None else None,
                float(animal.score) if animal.score is not None else None,
                float(animal.rating) if animal.rating is not None else None,
                str(animal.badge) if animal.badge is not None else None,
                float(animal.difficulty) if animal.difficulty is not None else None,
                str(animal.datetime),
                int(animal.furType) if animal.furType is not None else None,
                int(animal.lodge) if animal.lodge is not None else None,
                int(animal.reserve) if animal.reserve is not None else None
            ))

        conn.commit()
        conn.close()

    def trophyAnimals(self, query: dict = {}) -> List[TrophyAnimal]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        _lodgesIds = []
        _reservesAndOr = []
        _reservesIds = []
        _badgesAndOr = []
        _badgesIds = []
        _animalsAndOr = []
        _animalsIds = []

        if query != {}:
            _lodgesIds = query.get('lodges', [])
            _reservesAndOr = query.get('reservesAndOr', [])
            _reservesIds = query.get('reserves', [])
            _badgesAndOr = query.get('badgesAndOr', [])
            _badgesIds = query.get('badges', [])
            _animalsAndOr = query.get('animalsAndOr', [])
            _animalsIds = query.get('animals', [])

        where_clauses = []
        params = []

        if _lodgesIds:
            placeholders = ','.join(['?' for _ in _lodgesIds])
            where_clauses.append(f"lodge IN ({placeholders})")
            params.extend(_lodgesIds)

        if _reservesIds:
            placeholders = ','.join(['?' for _ in _reservesIds])
            where_clauses.append(f"reserve IN ({placeholders})")
            params.extend(_reservesIds)

        if _badgesIds:
            placeholders = ','.join(['?' for _ in _badgesIds])
            where_clauses.append(f"badge IN ({placeholders})")
            params.extend(_badgesIds)

        if _animalsIds:
            placeholders = ','.join(['?' for _ in _animalsIds])
            where_clauses.append(f"type IN ({placeholders})")
            params.extend(_animalsIds)

        sql = "SELECT * FROM TrophyAnimals"
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)

        cursor.execute(sql, params)
        rows = cursor.fetchall()

        trophy_animals = []
        for row in rows:
            animal = TrophyAnimal(
                animalType=int(row[1]) if row[1] is not None else None,
                weight=float(row[2]) if row[2] is not None else None,
                gender=int(row[3]) if row[3] is not None else None,
                score=float(row[4]) if row[4] is not None else None,
                rating=float(row[5]) if row[5] is not None else None,
                badge=str(row[6]) if row[6] is not None else None,
                difficulty=float(row[7]) if row[7] is not None else None,
                datetime=row[8],
                furType=int(row[9]) if row[9] is not None else None,
                lodge=int(row[10]) if row[10] is not None else None,
                reserve=int(row[11]) if row[11] is not None else None
            )
            animal.id = row[0]
            trophy_animals.append(animal)

        conn.close()
        return trophy_animals

    def lodges(self) -> dict:
        animals = sorted(self.trophyAnimals(), key=lambda x: x.lodge)
        lodges = list(map(lambda t: t.lodge, animals))
        return {l: f'LODGE {l}' for l in lodges}