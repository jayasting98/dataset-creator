from typing import Any
import unittest
from unittest import mock

import datasets

from dataset_creator import loaders


class HuggingFaceLoaderTest(unittest.TestCase):
    def test_load__streaming_not_configured__loads_via_stream(self):
        config = {'path': 'path'}
        loader = loaders.HuggingFaceLoader[dict[str, Any]](config)
        def generator():
            yield {'message': 'Hello'}
            yield {'message': 'World!'}
        dataset = datasets.Dataset.from_generator(generator)
        with mock.patch('datasets.load_dataset') as mock_load_dataset:
            mock_load_dataset.return_value = dataset
            iterator = loader.load()
        mock_load_dataset.assert_called_once_with(path='path', streaming=True)
        self.assertEqual({'message': 'Hello'}, next(iterator))
        self.assertEqual({'message': 'World!'}, next(iterator))
        with self.assertRaises(StopIteration):
            next(iterator)
