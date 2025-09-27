from enum import Enum

class LodgeType(Enum):
    SPRING_CREEK = 1
    SASEKA_SAFARI = 2
    LAYTON_LAKE = 3

    def lodgeName(self) -> str:
            return self.name.replace("_", " ")

