import sqlite3
from pathlib import Path
from typing import List

from lib.model.animal_type import AnimalType
from lib.model.lodge import Lodge
from lib.model.lodge_type import LodgeType
from lib.model.medal import Medal
from lib.model.reserve import Reserve
from lib.model.trophy_animal import TrophyAnimal


class TrophyAnimalQuery:
    def __init__(self, db_path: Path):
        self.db_path = db_path

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

            reserveAnimalsSelectSql = """
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
                NULL as lodgeType,
                NULL as lodgeTypeId,
                NULL as reserve
                FROM AnimalsReserves
                """

            allAnimalsSql = (reserveAnimalsSelectSql
                             + f""" WHERE type NOT IN ({trophyTypesSubquery})""")

            match (5 in set(_medalsIds), bool(_reservesIds)):
                case (True, True):
                    reservePlaceholders = ','.join(['?' for _ in _reservesIds])
                    allAnimalsSql = (reserveAnimalsSelectSql
                                     + f""" JOIN AnimalMedal USING(type) 
                                                WHERE type NOT IN ({trophyTypesSubquery}) 
                                                AND reserve IN ({reservePlaceholders}) """)
                    allAnimalsParams.extend(_reservesIds)
                case (True, False):
                    allAnimalsSql = (reserveAnimalsSelectSql
                                     + f""" JOIN AnimalMedal USING(type)   
                                                WHERE type NOT IN ({trophyTypesSubquery})""")
                case (False, True):
                    reservePlaceholders = ','.join(['?' for _ in _reservesIds])
                    allAnimalsSql = (reserveAnimalsSelectSql
                                     + f""" WHERE type NOT IN ({trophyTypesSubquery})
                                                AND reserve IN ({reservePlaceholders}) """)
                    allAnimalsParams.extend(_reservesIds)
                case _:
                    pass

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
                lodge=Lodge(int(row[9]), LodgeType(row[10]), int(row[11])) if row[9] is not None else None,
                reserve=Reserve(int(row[12])) if row[12] is not None else None
            )
            animal.id = row[0]
            trophy_animals.append(animal)

        conn.close()
        return trophy_animals

    def lodges(self) -> dict:
        lodges: List[Lodge] = list(map(lambda t: t.lodge, self.trophyAnimals()))
        return {l.lodgeId: l.lodgeName() for l in lodges}
