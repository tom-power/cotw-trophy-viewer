from typing import List

from lib.model.preset import Preset


class DefaultPresetsLoader:
    @staticmethod
    def load() -> List[Preset]:
        return [layton_lakes_lodge_todo, great_one_todo_preset]

layton_lakes_lodge_todo = Preset(
    name="layton lakes todo",
    query={
        "lodges": [1],
        "reserves": [0 ,1],
        "medals": [],
        "animals": [],
        "reservesAndOr": "and",
        "medalsAndOr": "and",
        "animalsAndOr": "and",
        "allAnimals": True
    }
)

great_one_todo_preset = Preset(
    name="great one todo",
    query={
        "lodges": [],
        "reserves": [],
        "medals": [5],
        "animals": [],
        "reservesAndOr": "and",
        "medalsAndOr": "and",
        "animalsAndOr": "and",
        "allAnimals": True
    }
)
