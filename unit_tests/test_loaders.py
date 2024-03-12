import unittest
from unittest import mock

import datasets

from dataset_creator import loaders


class HuggingFaceLoaderTest(unittest.TestCase):
    def test_load__streaming_not_configured__loads_via_stream(self):
        config = {'path': 'path'}
        loader = loaders.HuggingFaceLoader(config)
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

    def test_load__skip_not_none__skips_before_loading(self):
        config = {'path': 'path'}
        loader = loaders.HuggingFaceLoader(config, skip=2)
        def generator():
            yield {'message': 'Hello'}
            yield {'message': 'World!'}
            yield {'message': 'It\'s'}
            yield {'message': 'a'}
            yield {'message': 'wonderful'}
            yield {'message': 'day!'}
        dataset = datasets.Dataset.from_generator(generator)
        with mock.patch('datasets.load_dataset') as mock_load_dataset:
            mock_load_dataset.return_value = dataset
            iterator = loader.load()
        mock_load_dataset.assert_called_once_with(path='path', streaming=True)
        self.assertEqual({'message': 'It\'s'}, next(iterator))
        self.assertEqual({'message': 'a'}, next(iterator))
        self.assertEqual({'message': 'wonderful'}, next(iterator))
        self.assertEqual({'message': 'day!'}, next(iterator))
        with self.assertRaises(StopIteration):
            next(iterator)
