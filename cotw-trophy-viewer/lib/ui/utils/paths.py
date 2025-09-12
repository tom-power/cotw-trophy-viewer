from pathlib import Path

from lib.deca.config import set_custom_save_path, reset_to_default_save_path, get_save_path


class Paths(object):
    def __init__(self, path: Path):
        self.path = path

    def __str__(self):
        return str(self.path)

    def getLoadPath(self):
        return self.path

    def updateLoadPath(self, new_path):
        self.path = new_path
        set_custom_save_path(new_path)

    def resetToDefaultPath(self, ):
        reset_to_default_save_path()
        self.path = get_save_path()