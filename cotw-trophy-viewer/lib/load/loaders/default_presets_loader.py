from typing import List

from lib.model.preset import Preset


class DefaultPresetsLoader:
    @staticmethod
    def load() -> List[Preset]:
        return [diamond_checklist_preset, layton_lakes_lodge_todo]


diamond_checklist_preset = Preset(
    name="diamond checklist",
    query={
        "lodges": [],
        "reserves": [],
        "medals": [0],
        "animals": [],
        "reservesAndOr": "and",
        "medalsAndOr": "and",
        "animalsAndOr": "and",
        "allAnimals": True
    }
)

layton_lakes_lodge_todo = Preset(
    name="layton lakes lodge todo",
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
