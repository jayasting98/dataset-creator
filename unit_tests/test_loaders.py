import unittest
from unittest import mock

from dataset_creator import loaders


class HuggingFaceLoaderTest(unittest.TestCase):
    def test_load__streaming_not_configured__loads_via_stream(self):
        config = {'path': 'path'}
        loader = loaders.HuggingFaceLoader[str](config)
        with mock.patch('datasets.load_dataset') as mock_load_dataset:
            mock_load_dataset.return_value = ['Hello', 'World!']
            iterator = loader.load()
        mock_load_dataset.assert_called_once_with(path='path', streaming=True)
        self.assertEqual('Hello', next(iterator))
        self.assertEqual('World!', next(iterator))
