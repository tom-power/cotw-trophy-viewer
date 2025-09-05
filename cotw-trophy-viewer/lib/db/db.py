import sqlite3 as sqlite

class Db:
    def __init__(self) -> None:
        self.conn = sqlite.connect('trophy_viewer.sqlite')

    def load()
