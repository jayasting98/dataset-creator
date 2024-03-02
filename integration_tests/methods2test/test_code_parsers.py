import json
import os
import unittest

from dataset_creator.methods2test import code_parsers


class CodeParserTest(unittest.TestCase):
    def setUp(self) -> None:
        grammar_file_pathname = 'java-grammar.so'
        language = 'java'
        self._parser = code_parsers.CodeParser(grammar_file_pathname, language)
        repo_dir_pathname = os.path.join('integration_tests', 'resources',
            'repositories', 'guess-the-number')
        self._focal_dir_pathname = os.path.join(repo_dir_pathname, 'src',
            'main', 'java', 'com', 'example', 'guessthenumber')
        self._test_dir_pathname = os.path.join(repo_dir_pathname, 'src',
            'test', 'java', 'com', 'example', 'guessthenumber')
        output_dir_pathname = os.path.join('integration_tests', 'resources',
            'expected_parser_outputs', 'guess-the-number')
        self._focal_output_dir_pathname = os.path.join(output_dir_pathname,
            'src', 'main', 'java', 'com', 'example', 'guessthenumber')
        self._test_output_dir_pathname = os.path.join(output_dir_pathname,
            'src', 'test', 'java', 'com', 'example', 'guessthenumber')

    def test_parse_file__typical_focal_file__parses_correctly(self):
        output_file_pathname = (os.path
            .join(self._focal_output_dir_pathname, 'ui', 'CommandLineUi.json'))
        code_file_pathname = (
            os.path.join(self._focal_dir_pathname, 'ui', 'CommandLineUi.java'))
        with open(output_file_pathname) as output_file:
            expected_parsed_classes = json.load(output_file)
        actual_parsed_classes = self._parser.parse_file(code_file_pathname)
        self.assertEqual(expected_parsed_classes, actual_parsed_classes)

    def test_parse_file__typical_test_file__parses_correctly(self):
        output_file_pathname = os.path.join(
            self._test_output_dir_pathname, 'ui', 'CommandLineUiTest.json')
        code_file_pathname = (os
            .path.join(self._test_dir_pathname, 'ui', 'CommandLineUiTest.java'))
        with open(output_file_pathname) as output_file:
            expected_parsed_classes = json.load(output_file)
        actual_parsed_classes = self._parser.parse_file(code_file_pathname)
        self.assertEqual(expected_parsed_classes, actual_parsed_classes)
