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

    def test_db_preset_add(self):
        test_query = {
            "lodges": [1, 2],
            "reserves": [3, 4],
            "medals": [1, 2],
            "animals": [5, 6],
            "reservesAndOr": "or",
            "medalsAndOr": "or",
            "animalsAndOr": "or",
            "allAnimals": False
        }

        self.db.presetAdd("test preset", test_query)

        presets = self.db.presets()
        self.assertEqual(3, len(presets))
        self.assertIn('test preset', presets.values())

        test_preset_id = None
        for preset_id, name in presets.items():
            if name == "test preset":
                test_preset_id = preset_id
                break

        self.assertIsNotNone(test_preset_id)
        retrieved_query = self.db.preset(test_preset_id)
        self.assertEqual(test_query, retrieved_query)

    def test_db_preset_add_duplicate_name(self):
        test_query1 = {"medals": [1], "allAnimals": True}
        test_query2 = {"medals": [2], "allAnimals": False}

        self.db.presetAdd("duplicate name", test_query1)
        initial_presets = self.db.presets()

        self.db.presetAdd("duplicate name", test_query2)
        final_presets = self.db.presets()

        self.assertEqual(len(initial_presets), len(final_presets))

        preset_id = None
        for preset_id, name in final_presets.items():
            if name == "duplicate name":
                break

        self.assertIsNotNone(preset_id)
        retrieved_query = self.db.preset(preset_id)
        self.assertEqual(test_query1, retrieved_query)

    def test_db_preset_remove(self):
        test_query = {
            "lodges": [1, 2],
            "reserves": [3, 4],
            "medals": [1, 2],
            "animals": [5, 6],
            "reservesAndOr": "or",
            "medalsAndOr": "or",
            "animalsAndOr": "or",
            "allAnimals": False
        }

        self.db.presetAdd("test preset to remove", test_query)

        presets_before = self.db.presets()
        self.assertEqual(3, len(presets_before))
        self.assertIn('test preset to remove', presets_before.values())

        preset_id_to_remove = None
        for preset_id, name in presets_before.items():
            if name == "test preset to remove":
                preset_id_to_remove = preset_id
                break

        self.assertIsNotNone(preset_id_to_remove)

        self.db.presetRemove(preset_id_to_remove)

        presets_after = self.db.presets()
        self.assertEqual(2, len(presets_after))
        self.assertNotIn('test preset to remove', presets_after.values())
        self.assertIn('layton lake lodge todo', presets_after.values())

    def test_db_preset_add_persists(self):
        test_query = {
            "lodges": [1, 2],
            "reserves": [3, 4],
            "medals": [1, 2],
            "animals": [5, 6],
            "reservesAndOr": "or",
            "medalsAndOr": "or",
            "animalsAndOr": "or",
            "allAnimals": False
        }

        self.db.presetAdd("test preset", test_query)

        presets = self.db.presets()
        self.assertEqual(3, len(presets))
        self.assertIn('test preset', presets.values())

        new_db_instance = getDb()
        presets = new_db_instance.presets()
        self.assertEqual(3, len(presets))
        self.assertIn('test preset', presets.values())

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
