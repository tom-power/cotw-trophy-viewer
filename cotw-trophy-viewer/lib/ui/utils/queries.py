
class Queries(object):

    def __init__(self):
        self.queryDict = {
        'lodges': [],
        'reservesAndOr': '',
        'reserves': [],
        'medalsAndOr': '',
        'medals': [],
        'animalsAndOr': '',
        'animals': [],
        'allAnimals': False,
    }

    def updateQuery(self, key, value):
        self.queryDict[key] = value

    def updateQueryFor(self, key):
        return lambda e: self.updateQuery(key, e.value)