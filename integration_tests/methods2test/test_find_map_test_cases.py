import os
import unittest

from dataset_creator.methods2test import find_map_test_cases


class FindMapTestCasesTest(unittest.TestCase):
    def test_find_test_files__typical_case__finds_correctly(self):
        root = os.path.join('integration_tests', 'resources', 'repositories',
            'guess-the-number')
        common_test_dir = os.path.join('src', 'test', 'java', 'com', 'example',
            'guessthenumber')
        expected_test_files = [
            os.path.join(common_test_dir, 'AppTest.java'),
            os.path.join(common_test_dir, 'logic', 'StandardLogicTest.java'),
            os.path.join(common_test_dir, 'ui', 'CommandLineUiTest.java'),
        ]
        actual_test_files = find_map_test_cases.find_test_files(root)
        self.assertEqual(expected_test_files, actual_test_files)

    def test_find_java_files__typical_case__finds_correctly(self):
        root = os.path.join('integration_tests', 'resources', 'repositories',
            'guess-the-number')
        common_focal_dir = os.path.join('src', 'main', 'java', 'com', 'example',
            'guessthenumber')
        common_test_dir = os.path.join('src', 'test', 'java', 'com', 'example',
            'guessthenumber')
        expected_java_files = [
            os.path.join(common_focal_dir, 'App.java'),
            os.path.join(common_focal_dir, 'logic', 'GameState.java'),
            os.path.join(common_focal_dir, 'logic', 'Logic.java'),
            os.path.join(common_focal_dir, 'logic', 'StandardLogic.java'),
            os.path.join(common_focal_dir, 'ui', 'CommandLineUi.java'),
            os.path.join(common_focal_dir, 'ui', 'UserInterface.java'),
            os.path.join(common_test_dir, 'AppTest.java'),
            os.path.join(common_test_dir, 'logic', 'StandardLogicTest.java'),
            os.path.join(common_test_dir, 'ui', 'CommandLineUiTest.java'),
        ]
        actual_java_files = find_map_test_cases.find_java_files(root)
        self.assertEqual(expected_java_files, actual_java_files)

    def test_find_focal_files__typical_case__finds_correctly(self):
        common_focal_dir = os.path.join('src', 'main', 'java', 'com', 'example',
            'guessthenumber')
        common_test_dir = os.path.join('src', 'test', 'java', 'com', 'example',
            'guessthenumber')
        test_files = [
            os.path.join(common_test_dir, 'AppTest.java'),
            os.path.join(common_test_dir, 'logic', 'StandardLogicTest.java'),
            os.path.join(common_test_dir, 'ui', 'CommandLineUiTest.java'),
        ]
        java_files = [
            os.path.join(common_focal_dir, 'App.java'),
            os.path.join(common_focal_dir, 'logic', 'GameState.java'),
            os.path.join(common_focal_dir, 'logic', 'Logic.java'),
            os.path.join(common_focal_dir, 'logic', 'StandardLogic.java'),
            os.path.join(common_focal_dir, 'ui', 'CommandLineUi.java'),
            os.path.join(common_focal_dir, 'ui', 'UserInterface.java'),
            os.path.join(common_test_dir, 'AppTest.java'),
            os.path.join(common_test_dir, 'logic', 'StandardLogicTest.java'),
            os.path.join(common_test_dir, 'ui', 'CommandLineUiTest.java'),
        ]
        expected_focal_files = [
            os.path.join(common_focal_dir, 'App.java'),
            os.path.join(common_focal_dir, 'logic', 'GameState.java'),
            os.path.join(common_focal_dir, 'logic', 'Logic.java'),
            os.path.join(common_focal_dir, 'logic', 'StandardLogic.java'),
            os.path.join(common_focal_dir, 'ui', 'CommandLineUi.java'),
            os.path.join(common_focal_dir, 'ui', 'UserInterface.java'),
        ]
        actual_focal_files = (
            find_map_test_cases.find_focal_files(java_files, test_files))
        self.assertEqual(expected_focal_files, actual_focal_files)

    def test_map_test_to_focal_files__typical_case__finds_correctly(self):
        common_focal_dir = os.path.join('src', 'main', 'java', 'com', 'example',
            'guessthenumber')
        common_test_dir = os.path.join('src', 'test', 'java', 'com', 'example',
            'guessthenumber')
        app_test_file = os.path.join(common_test_dir, 'AppTest.java')
        standard_logic_test_file = (
            os.path.join(common_test_dir, 'logic', 'StandardLogicTest.java'))
        command_line_ui_test_file = (
            os.path.join(common_test_dir, 'ui', 'CommandLineUiTest.java'))
        test_files = [
            app_test_file,
            standard_logic_test_file,
            command_line_ui_test_file,
        ]
        app_focal_file = os.path.join(common_focal_dir, 'App.java')
        standard_logic_focal_file = (
            os.path.join(common_focal_dir, 'logic', 'StandardLogic.java'))
        command_line_ui_focal_file = (
            os.path.join(common_focal_dir, 'ui', 'CommandLineUi.java'))
        focal_files = [
            app_focal_file,
            os.path.join(common_focal_dir, 'logic', 'GameState.java'),
            os.path.join(common_focal_dir, 'logic', 'Logic.java'),
            standard_logic_focal_file,
            command_line_ui_focal_file,
            os.path.join(common_focal_dir, 'ui', 'UserInterface.java'),
        ]
        expected_test_to_focal_files = {
            app_test_file: app_focal_file,
            standard_logic_test_file: standard_logic_focal_file,
            command_line_ui_test_file: command_line_ui_focal_file,
        }
        actual_test_to_focal_files = (find_map_test_cases
            .map_test_to_focal_files(focal_files, test_files))
        self.assertEqual(
            expected_test_to_focal_files, actual_test_to_focal_files)
