from typing import List


class DefaultPresetsLoader:
    def load(self) -> List[dict]:
        diamond_checklist_preset = {
            "name": "diamond checklist",
            "query": {
                "lodges": [],
                "reserves": [],
                "medals": [0],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }
        }
        return [diamond_checklist_preset]
