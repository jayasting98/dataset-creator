import os
from typing import Generator
from typing import Iterator
import unittest

from dataset_creator import loaders


class JsonlFileLoaderTest(unittest.TestCase):
    def test_load__typical_case__loads_correctly(self):
        pathname = (
            os.path.join('integration_tests', 'resources', 'samples.jsonl'))
        loader = loaders.JsonlFileLoader(pathname)
        actual_iter = loader.load()
        self.assertIsInstance(actual_iter, Iterator)
        self.assertNotIsInstance(actual_iter, Generator)
        self.assertEqual(dict(Hello='World!', num=4), next(actual_iter))
        self.assertEqual(dict(Hello='there', num=2), next(actual_iter))
        with self.assertRaises(StopIteration):
            next(actual_iter)
