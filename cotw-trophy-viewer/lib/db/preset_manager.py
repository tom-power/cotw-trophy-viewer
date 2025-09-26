import json
import sqlite3
from pathlib import Path
from typing import List

from lib.model.preset import Preset


class PresetManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._create_preset_table()

    def _create_preset_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Preset (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                query TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

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

    def presetInit(self, default_presets: List[Preset]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM Preset')
        if cursor.fetchone()[0] == 0:
            for preset in default_presets:
                cursor.execute(
                    'INSERT INTO Preset (name, query) VALUES (?, ?)',
                    (preset.name, json.dumps(preset.query))
                )

        conn.commit()
        conn.close()

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


