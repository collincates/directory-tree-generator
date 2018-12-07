import unittest
from unittest.mock import patch

import os
import shutil

from tvprojectfoldersetup import DirectoryStructure, folder_names


class DirectoryStructureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_object = DirectoryStructure()
        cls.test_object.show_name = 'Test'
        cls.test_object.season = '10'
        cls.test_object.num_eps = [
            '01', '02', '03', '04', '05', '06', '07', '08', '09', '10'
        ]

    @classmethod
    def tearDownClass(cls):
        # Remove directories that are made during the tests
        shutil.rmtree(os.path.join(os.getcwd(), cls.test_object.show_name, ''))


    def test_folder_names_exist(self):
        self.assertEqual(len(folder_names), 2)

    def test_DirectoryStructure_instance_exists(self):
        self.assertTrue(self.test_object)
        self.assertTrue(self.test_object.show_name)
        self.assertTrue(self.test_object.season)
        self.assertTrue(self.test_object.num_eps)

    @patch('builtins.input', lambda _: 'Test')
    def test_set_up_show_name(self):
        self.test_object.set_up_show_name()
        self.assertEqual(self.test_object.show_name, 'Test')

    @patch('builtins.input', lambda _: '1')
    def test_set_up_season_number_with_integer(self):
        self.test_object.set_up_season_number()
        self.assertEqual(self.test_object.season, '1')

    # Implement and test two-digit layout with a leading zero
    @unittest.SkipTest
    @patch('builtins.input', lambda _: '1')
    def test_set_up_season_number_with_integer(self):
        self.test_object.set_up_season_number()
        self.assertEqual(self.test_object.season, '1')

    @unittest.SkipTest
    @patch('builtins.input', 'String')
    def test_set_up_season_number_with_string(self):
        self.assertRaises(ValueError, self.test_object.set_up_season_number())

    @patch('builtins.input', lambda _: '10')
    def test_set_up_episode_qty_with_integer(self):
        self.test_object.set_up_episode_qty()
        self.assertEqual(
            self.test_object.num_eps,
            ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
        )

    @unittest.SkipTest
    @patch('builtins.input', 'String')
    def test_set_up_episode_qty_with_string(self):
        self.assertRaises(ValueError, self.test_object.set_up_episode_qty())

    @patch('builtins.input', lambda _: '1')
    def test_decide_folder_heirarchy_category_first(self):
        self.test_object.decide_folder_heirarchy()
        self.assertEqual(self.test_object.order, 'by_category')

    @patch('builtins.input', lambda _: '2')
    def test_decide_folder_heirarchy_episode_first(self):
        self.test_object.decide_folder_heirarchy()
        self.assertEqual(self.test_object.order, 'by_episode')

    @patch('builtins.input', lambda _: '3')
    def test_decide_folder_heirarchy_no_episode(self):
        self.test_object.decide_folder_heirarchy()
        self.assertEqual(self.test_object.order, 'category_only')

    @unittest.SkipTest
    @patch('builtins.input', lambda _: 'String')
    def test_decide_folder_heirarchy_invalid_retries(self):
        try:
            self.assertRaises(RecursionError, self.test_object.decide_folder_heirarchy())
        except RecursionError:
            fail('this failed')

    def test_add_delete_folders_sets_attribute_cat_folders(self):
        self.test_object.add_delete_folders()
        self.assertTrue(self.test_object.cat_folders)

    @unittest.SkipTest
    @patch('builtins.input', lambda _: 'SAVE')
    def test_confirm_layout_with_input_as_save_calls_create(self):
        self.test_object.confirm_layout()
        self.assertTrue(self.test_object.create())
        # with patch(self.test_object.confirm_layout()) as mock:

    def test_create_directory_tree_builds_ep_folders_attribute(self):
        self.test_object.order = 'by_category'
        self.test_object.create_directory_tree(open_in_finder=False)
        self.assertTrue(self.test_object.ep_folders)
        self.assertEqual(self.test_object.ep_folders, [
            'Episode 1001',
            'Episode 1002',
            'Episode 1003',
            'Episode 1004',
            'Episode 1005',
            'Episode 1006',
            'Episode 1007',
            'Episode 1008',
            'Episode 1009',
            'Episode 1010'
            ]
        )

    def test_create_directory_tree_builds_actual_folders(self):
        self.test_object.order = 'by_category'
        self.test_object.create_directory_tree(open_in_finder=False)
        self.assertTrue(os.path.join(os.getcwd(), self.test_object.show_name, ''))

# if __name__ == "__main__":
#     unittest.main()
