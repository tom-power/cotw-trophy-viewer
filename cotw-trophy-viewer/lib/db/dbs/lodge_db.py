import sqlite3
from pathlib import Path
from typing import List


class LodgeDb:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._create_tables()

    def _create_tables(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS Lodges')
        cursor.execute('''               
               CREATE TABLE Lodges (
                   lodgeId INTEGER PRIMARY KEY,
                   lodgeType INTEGER,
                   lodgeTypeId INTEGER
               )
           ''')

        conn.commit()
        conn.close()


    def insert_lodges(self, lodges: List[dict]) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Lodges')

        for lodge in lodges:
            cursor.execute('''
                INSERT INTO Lodges
                (lodgeId, lodgeType, lodgeTypeId)
                VALUES (?, ?, ?)
            ''', (
                int(lodge['lodgeId']) if lodge['lodgeId'] is not None else None,
                int(lodge['lodgeType']) if lodge['lodgeType'] is not None else None,
                int(lodge['lodgeTypeId']) if lodge['lodgeTypeId'] is not None else None
            ))

        conn.commit()
        conn.close()
