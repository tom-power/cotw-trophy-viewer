import unittest

from lib.load.trophy_animal_mapper import TrophyAnimalMapper


class TestTrophyAnimalMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = TrophyAnimalMapper()

    def test_fromTrophyHybrids_filters_lodge_id_zero(self):
        trophy_lodge = {
            "TrophyHybrids": {
                "Trophies": [
                    {
                        "LodgeId": 0,  # Should be filtered out
                        "TrophyHybrid": {
                            "TrophyAnimals": [
                                {"Type": 123, "Weight": 100.0}
                            ]
                        }
                    },
                    {
                        "LodgeId": 1,  # Should be included
                        "TrophyHybrid": {
                            "TrophyAnimals": [
                                {"Type": 456, "Weight": 200.0}
                            ]
                        }
                    }
                ]
            }
        }

        self.mapper.add(trophy_lodge)
        result = self.mapper.map()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].lodge.lodgeId, 1)
        self.assertEqual(result[0].weight, 200.0)

    def test_fromTrophyAnimals_filters_lodge_id_zero(self):
        trophy_lodge = {
            "TrophyAnimals": {
                "Trophies": [
                    {
                        "LodgeId": 0,  # Should be filtered out
                        "TrophyAnimal": {"Type": 123, "Weight": 100.0}
                    },
                    {
                        "LodgeId": 2,  # Should be included
                        "TrophyAnimal": {"Type": 456, "Weight": 300.0}
                    }
                ]
            }
        }

        self.mapper.add(trophy_lodge)
        result = self.mapper.map()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].lodge.lodgeId, 2)
        self.assertEqual(result[0].weight, 300.0)


if __name__ == '__main__':
    unittest.main()
