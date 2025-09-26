import unittest
from lib.load.TrophyAnimalMapper import TrophyAnimalMapper


class TestTrophyAnimalMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = TrophyAnimalMapper()

    def test_fromTrophyHybrids_filters_lodge_id_zero(self):
        """Test that trophies with LodgeId == 0 are filtered out from TrophyHybrids"""
        # Arrange
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

        # Act
        result = self.mapper.map(trophy_lodge)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].lodge, 1)
        self.assertEqual(result[0].weight, 200.0)

    def test_fromTrophyAnimals_filters_lodge_id_zero(self):
        """Test that trophies with LodgeId == 0 are filtered out from TrophyAnimals"""
        # Arrange
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

        # Act
        result = self.mapper.map(trophy_lodge)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].lodge, 2)
        self.assertEqual(result[0].weight, 300.0)


if __name__ == '__main__':
    unittest.main()