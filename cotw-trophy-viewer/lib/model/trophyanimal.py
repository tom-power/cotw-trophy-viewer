
class TrophyAnimal:
    type: ""

    def __init__(self, type, weight, gender, score, rating, difficulty, datetime, furType, lodge, reserve):
        self.type = type
        self.weight = weight
        self.gender = gender
        self.score = score
        self.rating = rating
        self.difficulty = difficulty
        self.datetime = datetime
        self.furType = furType
        self.lodge = lodge
        self.reserve = reserve

    def toString(self):
        return "["+self.datetime+"] | Weight: "+str(self.weight)+" | Fur: "+str(self.furType)+" | Gender: "+str(self.gender)+" | Score: "+str(self.score)+" | Rating: "+str(self.rating)+" | Cash: "+str(self.cash)+" | XP: "+str(self.xp)+" | RatingIcon: "+str(self.ratingIcon)+" | Difficulty: "+str(self.difficulty)+""

    def getID(self):
        return str(self.weight)+'-'+str(self.rating)+'-'+str(self.difficulty)