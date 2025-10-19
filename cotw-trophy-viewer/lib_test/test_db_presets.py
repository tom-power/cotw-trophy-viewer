import os
import sys
import unittest

from lib_test.fixtures import getDb

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class TestAllPresetsFunctions(unittest.TestCase):

    def setUp(self):
        self.db = getDb()

    def tearDown(self):
        for p in self.db.presets():
            self.db.presetRemove(p)

    def test_db_preset(self):
        presets_list = self.db.presets()
        layton_lakes_preset_id = None
        for preset_id, name in presets_list.items():
            if name == "layton lake lodge todo":
                layton_lakes_preset_id = preset_id
                break

        presets = self.db.preset(layton_lakes_preset_id)

        laytonLakesTodo = \
            {
                "lodges": [1],
                "reserves": [0, 1],
                "medals": [],
                "animals": [],
                "reservesAndOr": "and",
                "medalsAndOr": "and",
                "animalsAndOr": "and",
                "allAnimals": True
            }

        self.assertEqual(laytonLakesTodo, presets)

    def test_db_presets(self):
        presets = self.db.presets()
        self.assertEqual(2, len(presets))
        self.assertIn('layton lake lodge todo', presets.values())
        self.assertIn('great one todo', presets.values())


    def test_db_preset_inserts_defaults_once(self):
        presets = self.db.presets()
        self.assertEqual(2, len(presets))
        self.assertIn('layton lake lodge todo', presets.values())

        preset_id_to_remove = None
        for preset_id, name in presets.items():
            if name == 'layton lake lodge todo':
                preset_id_to_remove = preset_id
                break

        self.db.presetRemove(preset_id_to_remove)

        new_db_instance = getDb()
        presets = new_db_instance.presets()
        self.assertEqual(1, len(presets))
        self.assertNotIn('layton lake lodge todo', presets.values())
