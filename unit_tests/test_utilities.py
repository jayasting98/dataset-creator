import os
from typing import Generator
from typing import Iterator
import unittest

from dataset_creator import utilities


class GeneratorFunctionIteratorTest(unittest.TestCase):
    def test___init____typical_case__creates_iterator(self):
        def generator_function():
            yield 'Hello'
            yield 'World!'
        iterator = utilities.GeneratorFunctionIterator(generator_function)
        self.assertIsInstance(generator_function(), Generator)
        self.assertNotIsInstance(iterator, Generator)
        self.assertIsInstance(iterator, Iterator)
        self.assertIsInstance(iter(iterator), Iterator)
        self.assertEqual('Hello', next(iterator))
        self.assertEqual('World!', next(iterator))
        with self.assertRaises(StopIteration):
            next(iterator)


class WorkingDirectoryTest(unittest.TestCase):
    def test___typical_case__executes_in_respective_working_directories(self):
        current_working_directory = os.getcwd()
        with utilities.WorkingDirectory('/tmp'):
            self.assertEqual('/tmp', os.getcwd())
        self.assertEqual(current_working_directory, os.getcwd())


class UtilitiesTest(unittest.TestCase):
    def test_space_out_snake_case__non_snake_case_input__leaves_unchanged(self):
        x = 'testSpaceOutSnakeCase'
        expected_spaced_out_str = 'testSpaceOutSnakeCase'
        actual_spaced_out_str = utilities.space_out_snake_case(x)
        self.assertEqual(expected_spaced_out_str, actual_spaced_out_str)

    def test_space_out_snake_case__snake_case_input__spaces_out(self):
        x = 'test_space_out_snake_case'
        expected_spaced_out_str = 'test space out snake case'
        actual_spaced_out_str = utilities.space_out_snake_case(x)
        self.assertEqual(expected_spaced_out_str, actual_spaced_out_str)

    def test_space_out_snake_case__consecutive_underscore__one_space(self):
        x = 'test__space__out__snake__case'
        expected_spaced_out_str = 'test space out snake case'
        actual_spaced_out_str = utilities.space_out_snake_case(x)
        self.assertEqual(expected_spaced_out_str, actual_spaced_out_str)
