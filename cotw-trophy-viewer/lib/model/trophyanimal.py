import uuid

class TrophyAnimal:
    type: ""

    def __init__(self, animalType, weight, gender, rating, medal, difficulty, datetime, furType, lodge, reserve):
        self.id = uuid.uuid4()
        self.type: int = animalType
        self.weight: float = weight
        self.gender: int = gender
        self.rating: float = rating
        self.medal: float = medal
        self.difficulty: float = difficulty
        self.datetime = datetime
        self.furType: int = furType
        self.lodge: int = lodge
        self.reserve: int = reserve
