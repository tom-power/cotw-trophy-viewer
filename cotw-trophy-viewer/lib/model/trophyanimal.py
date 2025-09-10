import uuid


class TrophyAnimal:
    type: ""

    def __init__(self, animalType, weight, gender, score, rating, difficulty, datetime, furType, lodge, reserve):
        self.id = uuid.uuid4()
        self.type = animalType
        self.weight = weight
        self.gender = gender
        self.score = score
        self.rating = rating
        self.difficulty = difficulty
        self.datetime = datetime
        self.furType = furType
        self.lodge = lodge
        self.reserve = reserve
