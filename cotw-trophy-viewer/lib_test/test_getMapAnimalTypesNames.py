import unittest

from lib.load.mapAnimalTypesNames import getMapAnimalTypeNames


def _to_unsigned_32bit(n):
    return n % (1 << 32)


class TestGetMapAnimalTypesFunctions(unittest.TestCase):
    
    def test_getMapAnimalTypes(self):
        lookup = getMapAnimalTypeNames()
        self.assertEqual('FALLOW DEER', lookup(1511159411))
        self.assertEqual('SALTWATER CROCODILE', lookup(1443188410))
        self.assertEqual('EUROPEAN RABBIT', lookup(_to_unsigned_32bit(-715943829)))

    def test_getMapAnimalTypesUnknown(self):
        lookup = getMapAnimalTypeNames()
        self.assertEqual('123', lookup(123))
