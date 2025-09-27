from enum import Enum

class LodgeType(Enum):
    SPRING_CREEK_MANOR = 1
    SASEKA_SAFARI = 2
    LAYTON_LAKES = 3

    def lodgeName(self) -> str:
            return self.name.replace("_", " ")

