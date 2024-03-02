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
