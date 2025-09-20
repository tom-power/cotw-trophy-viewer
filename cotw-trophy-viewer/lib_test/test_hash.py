import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from lib.deca.hashes import hash32_func


class TestGetMapAnimalTypesFunctions(unittest.TestCase):

    def _hashCheck(self, names, hashedInt):
        print()
        for n in names:
            print(f"{n}")
            if hash32_func(n) == hashedInt:
                print(f"✓ FOUND MATCH for input '{n}'")
                return
        self.fail("No matching hash found")

    def test_hashFallowDeer(self):
        # names = ["FallowDeer", "fallow_deer", "FALLOW_DEER", "fallowdeer", "animal_fallowdeer_name",
        #          "Fallow Deer", "fallow deer", "AnimalFallowDeer", "animal_fallow_deer"]
        names = ["fallow_deer"]

        self._hashCheck(names, 1511159411)

    def test_hashSaltie(self):
        # names = ["SALTWATER_CROCODILE", "saltwater_crocodile"]
        names = ["saltwater_crocodile"]

        self._hashCheck(names, 1443188410)

    def test_hashEuroRabbit(self):
        names = [
            "eu_rabbit"
        ]
        # names = [
        #     "EUROPEANRABBIT", "EUROPEAN_RABBIT", "europeanrabbit", "european_rabbit", "animal_europeanrabbit_name",
        #     "EuropeanRabbit", "europeanRabbit", "European_Rabbit", "european_Rabbit",
        #     "EUROPEANRABBITNAME", "europeanrabbitname", "european_rabbit_name", "EUROPEAN_RABBIT_NAME",
        #     "animal_european_rabbit", "AnimalEuropeanRabbit", "animalEuropeanRabbit",
        #     "rabbit_european", "RabbitEuropean", "rabbitEuropean", "RABBIT_EUROPEAN",
        #     "european rabbit", "European rabbit", "european rabbit name", "European Rabbit Name",
        #     "EURABBIT", "EU_RABBIT", "eurabbit", "eu_rabbit", "animal_eurabbit_name",
        #     "EuRabbit", "euRabbit", "Eu_Rabbit", "eu_Rabbit",
        #     "EURABBITNAME", "eurabbitname", "eu_rabbit_name", "EU_RABBIT_NAME",
        #     "animal_eu_rabbit", "AnimalEuRabbit", "animalEuRabbit",
        #     "rabbit_eu", "RabbitEu", "rabbitEu", "RABBIT_EU",
        #     "eu rabbit", "Eu rabbit", "eu rabbit name", "Eu Rabbit Name",
        #     "EURORABBIT", "EURO_RABBIT", "eurorabbit", "euro_rabbit", "animal_eurorabbit_name",
        #     "EuroRabbit", "euroRabbit", "Euro_Rabbit", "euro_Rabbit",
        #     "EURORABBITNAME", "eurorabbitname", "euro_rabbit_name", "EURO_RABBIT_NAME",
        #     "animal_euro_rabbit", "AnimalEuroRabbit", "animalEuroRabbit",
        #     "rabbit_euro", "RabbitEuro", "rabbitEuro", "RABBIT_EURO",
        #     "euro rabbit", "Euro rabbit", "euro rabbit name", "Euro Rabbit Name"
        # ]

        self._hashCheck(names, _to_unsigned_32bit(-715943829))

    def test_hashMerriamTurkey(self):
        names = [
            "wild_turkey"
        ]

        self._hashCheck(names, _to_unsigned_32bit(-680325971))

    def test_hashRockyMountainElk(self):
        names = [
            "rockymountain_elk"
        ]

        self._hashCheck(names, _to_unsigned_32bit(1162399024))


    def test_hashEgKangaroo(self):
        names = ["eastern_grey_kangaroo"]
        # names = [
        #     "eg_kangaroo", "eastern_grey_kangaroo", "eastern greykangaroo", "eastern grey kangaroo",
        #     "eastern_grey_kangaroo", "easternGreyKangaroo", "EasternGreyKangaroo", "EG_KANGAROO",
        #     "egKangaroo", "EgKangaroo", "kangaroo_eastern_grey", "kangaroo_eg", "kangarooeg",
        #     "kangaroo_eastern_grey", "kangaroo eastern grey", "kangarooegkangaroo", "kangaroo_eg_kangaroo",
        #     "animal_eastern_grey_kangaroo", "animal_eg_kangaroo", "animalEgKangaroo"
        # ]

        self._hashCheck(names, _to_unsigned_32bit(-1512662627))


def _to_unsigned_32bit(n):
    return n % (1 << 32)
