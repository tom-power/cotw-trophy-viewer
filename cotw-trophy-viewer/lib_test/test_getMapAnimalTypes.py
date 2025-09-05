import unittest

from lib.load.mapAnimalTypes import getMapAnimalTypes


class TestGetMapAnimalTypesFunctions(unittest.TestCase):
    
    def test_getMapAnimalTypes(self):
        lookup = getMapAnimalTypes()
        self.assertEqual('FALLOW DEER', lookup(1511159411))

    def test_getMapAnimalTypesUnknown(self):
        lookup = getMapAnimalTypes()
        self.assertEqual('123', lookup(123))
