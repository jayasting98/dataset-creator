import json
import os
import unittest

from dataset_creator.methods2test import find_map_test_cases


class FindMapTestCasesTest(unittest.TestCase):
    def setUp(self) -> None:
        self._root = os.path.join('integration_tests', 'resources',
            'repositories', 'guess-the-number')
        self._focal_dir = os.path.join('src', 'main', 'java', 'com', 'example',
            'guessthenumber')
        self._test_dir = os.path.join('src', 'test', 'java', 'com', 'example',
            'guessthenumber')
        self._app_focal_file = os.path.join(self._focal_dir, 'App.java')
        self._game_state_focal_file = (
            os.path.join(self._focal_dir, 'logic', 'GameState.java'))
        self._logic_focal_file = (
            os.path.join(self._focal_dir, 'logic', 'Logic.java'))
        self._standard_logic_focal_file = (
            os.path.join(self._focal_dir, 'logic', 'StandardLogic.java'))
        self._command_line_ui_focal_file = (
            os.path.join(self._focal_dir, 'ui', 'CommandLineUi.java'))
        self._user_interface_focal_file = (
            os.path.join(self._focal_dir, 'ui', 'UserInterface.java'))
        self._app_test_file = os.path.join(self._test_dir, 'AppTest.java')
        self._standard_logic_test_file = (
            os.path.join(self._test_dir, 'logic', 'StandardLogicTest.java'))
        self._command_line_ui_test_file = (
            os.path.join(self._test_dir, 'ui', 'CommandLineUiTest.java'))
        self._java_files = [
            self._app_focal_file,
            self._game_state_focal_file,
            self._logic_focal_file,
            self._standard_logic_focal_file,
            self._command_line_ui_focal_file,
            self._user_interface_focal_file,
            self._app_test_file,
            self._standard_logic_test_file,
            self._command_line_ui_test_file,
        ]
        self._focal_files = [
            self._app_focal_file,
            self._game_state_focal_file,
            self._logic_focal_file,
            self._standard_logic_focal_file,
            self._command_line_ui_focal_file,
            self._user_interface_focal_file,
        ]
        self._test_files = [
            self._app_test_file,
            self._standard_logic_test_file,
            self._command_line_ui_test_file,
        ]
        self._output_dir_pathname = os.path.join('integration_tests',
            'resources', 'expected_focal_method_samples', 'guess-the-number')

    def test_find_test_files__typical_case__finds_correctly(self):
        expected_test_files = self._test_files
        actual_test_files = find_map_test_cases.find_test_files(self._root)
        self.assertEqual(expected_test_files, actual_test_files)

    def test_find_java_files__typical_case__finds_correctly(self):
        expected_java_files = self._java_files
        actual_java_files = find_map_test_cases.find_java_files(self._root)
        self.assertEqual(expected_java_files, actual_java_files)

    def test_find_focal_files__typical_case__finds_correctly(self):
        expected_focal_files = self._focal_files
        actual_focal_files = (find_map_test_cases
            .find_focal_files(self._java_files, self._test_files))
        self.assertEqual(expected_focal_files, actual_focal_files)

    def test_map_test_to_focal_files__typical_case__finds_correctly(self):
        expected_test_to_focal_files = {
            self._app_test_file: self._app_focal_file,
            self._standard_logic_test_file: self._standard_logic_focal_file,
            self._command_line_ui_test_file: self._command_line_ui_focal_file,
        }
        actual_test_to_focal_files = (find_map_test_cases
            .map_test_to_focal_files(self._focal_files, self._test_files))
        self.assertEqual(
            expected_test_to_focal_files, actual_test_to_focal_files)

    def test_find_focal_file_method_samples__typical_case__finds_correctly(
        self,
    ):
        simplified_focal_methods = [
            {
                'identifier': 'doSomething0',
            },
            {
                'identifier': 'doSomething1',
            },
        ]
        simplified_test_methods = [
            {
                'identifier': 'testDoSomething0',
                'invocations': [
                    'doSomething0',
                    'doSomething1',
                ],
            },
            {
                'identifier': 'shouldDoSomething0',
                'invocations': [
                    'doSomething0',
                ],
            },
            {
                'identifier': 'shouldDoSomething1',
                'invocations': [
                    'doSomething0',
                    'doSomething1',
                ],
            },
            {
                'identifier': 'shouldDoSomething1',
                'invocations': [
                    'doSomething1',
                ],
            },
        ]
        expected_focal_file_method_samples = [
            {
                'focal_method': {
                    'identifier': 'doSomething0',
                },
                'test_methods': [
                    {
                        'identifier': 'testDoSomething0',
                        'invocations': [
                            'doSomething0',
                            'doSomething1',
                        ],
                    },
                    {
                        'identifier': 'shouldDoSomething0',
                        'invocations': [
                            'doSomething0',
                        ],
                    },
                ],
            },
            {
                'focal_method': {
                    'identifier': 'doSomething1',
                },
                'test_methods': [
                    {
                        'identifier': 'shouldDoSomething1',
                        'invocations': [
                            'doSomething1',
                        ],
                    },
                ],
            },
        ]
        actual_focal_file_method_samples = (find_map_test_cases
            .find_focal_file_method_samples(
                simplified_focal_methods, simplified_test_methods))
        self.assertEqual(expected_focal_file_method_samples,
            actual_focal_file_method_samples)

    def test_find_focal_method_samples__typical_case__finds_correctly(self):
        output_file_pathname = (
            os.path.join(self._output_dir_pathname, 'typical_case.json'))
        grammar_file_pathname = 'java-grammar.so'
        language = 'java'
        with open(output_file_pathname) as output_file:
            expected_focal_method_samples = json.load(output_file)
        actual_focal_method_samples = (find_map_test_cases
            .find_focal_method_samples(
                self._root, grammar_file_pathname, language))
        self.assertEqual(
            expected_focal_method_samples, actual_focal_method_samples)
