import unittest

from lib.load.trophy_animal_mapper import TrophyAnimalMapper
from lib.model.lodge_type import LodgeType


class TestTrophyAnimalMapperLodge(unittest.TestCase):
    def setUp(self):
        self.mapper = TrophyAnimalMapper()

    def test_fromTrophyHybrids_get_lodge(self):
        trophy_lodge = {
            "TrophyHybrids": {
                "Trophies": [
                    {
                        "LodgeId": 1,
                        "TrophyHybrid": {
                            "TrophyAnimals": [
                                {"Type": 456, "Weight": 200.0}
                            ]
                        }
                    }
                ]
            },
            "TrophyLodges": {
                "Lodges": [
                    {
                        "Id": 1,
                        "TypeId": 1,
                        "Name": 0,
                        "Type": 3,
                    },
                ]
            }
        }

        self.mapper.add(trophy_lodge)
        result = self.mapper.map()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].lodge.lodgeId, 1)
        self.assertEqual(result[0].lodge.lodgeType, LodgeType.LAYTON_LAKES)
        self.assertEqual(result[0].lodge.lodgeTypeId, 1)
        self.assertEqual(result[0].weight, 200.0)

    def test_fromTrophyAnimals_get_lodge(self):
        trophy_lodge = {
            "TrophyAnimals": {
                "Trophies": [
                    {
                        "LodgeId": 2,
                        "TrophyAnimal": {"Type": 456, "Weight": 300.0}
                    }
                ]
            },
            "TrophyLodges": {
                "Lodges": [
                    {
                        "Id": 2,
                        "TypeId": 1,
                        "Name": 0,
                        "Type": 2,
                    }
                ]
            }
        }

        self.mapper.add(trophy_lodge)
        result = self.mapper.map()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].lodge.lodgeId, 2)
        self.assertEqual(result[0].lodge.lodgeType, LodgeType.SASEKA_SAFARI)
        self.assertEqual(result[0].lodge.lodgeTypeId, 1)
        self.assertEqual(result[0].weight, 300.0)
