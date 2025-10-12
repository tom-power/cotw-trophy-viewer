from typing import List


class LodgeMapper:
    def __init__(self):
        self.trophyLodges = None

    def add(self, trophyLodges: dict):
        self.trophyLodges = trophyLodges

    def map(self) -> List[dict]:
        lodges = []
        if "TrophyLodges" in self.trophyLodges and "Lodges" in self.trophyLodges["TrophyLodges"]:
            lodges_data = self.trophyLodges["TrophyLodges"]["Lodges"]
            for lodge in lodges_data:
                if "Id" in lodge and "Type" in lodge and "TypeId" in lodge:
                    lodges.append({
                        "lodgeId": lodge["Id"],
                        "lodgeType": lodge["Type"],
                        "lodgeTypeId": lodge["TypeId"]
                    })
        return lodges
