
class Queries(object):

    def __init__(self):
        self.queryDict = {
        'lodges': [],
        'reservesAndOr': 'or',
        'reserves': [],
        'badgesAndOr': 'or',
        'badges': [],
        'animalsAndOr': 'or',
        'animals': [],
        'animalsAll': False,
    }

    def updateQuery(self, key, value):
        self.queryDict[key] = value

    def updateQueryFor(self, key):
        return lambda e: self.updateQuery(key, e.value)