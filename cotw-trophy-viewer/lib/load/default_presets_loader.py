from typing import List
from lib.model.preset import Preset


class DefaultPresetsLoader:
    def load(self) -> List[Preset]:
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
        return [diamond_checklist_preset]
