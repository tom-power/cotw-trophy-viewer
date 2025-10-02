from pathlib import Path

from lib.deca.adf import load_adf


class LoadTrophyLodge:
    def __init__(self, loadPath: Path):
        self.loadPath = loadPath

    def lodges(self) -> dict:
        return self._load_trophy_lodges()

    def _load_trophy_lodges(self) -> dict:
        if self.loadPath is None:
            return {}
        adf = load_adf(self.loadPath, verbose=True).adf
        return adf.table_instance_values[0]
