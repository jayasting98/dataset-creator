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

    def test_load__limit_not_none__loads_up_to_limit(self):
        config = {'path': 'path'}
        loader = loaders.HuggingFaceLoader(config, limit=2)
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
        self.assertEqual({'message': 'Hello'}, next(iterator))
        self.assertEqual({'message': 'World!'}, next(iterator))
        with self.assertRaises(StopIteration):
            next(iterator)


class HuggingFaceMultiLoaderTest(unittest.TestCase):
    def test_load__streaming_not_configured__loads_via_stream(self):
        configs = [{'path': '1'}, {'path': '0'}, {'path': '3'}, {'path': '2'}]
        loader = loaders.HuggingFaceMultiLoader(configs)
        def do_side_effect(path: str, *args, **kwargs) -> datasets.Dataset:
            i = int(path)
            def generator():
                yield {'even': 2 * i, 'odd': 2 * i + 1}
                yield {'even': - (2 * i), 'odd': - (2 * i + 1)}
            dataset = datasets.Dataset.from_generator(generator)
            return dataset
        with mock.patch('datasets.load_dataset') as mock_load_dataset:
            mock_load_dataset.side_effect = do_side_effect
            iterator = loader.load()
        calls = mock_load_dataset.call_args_list
        self.assertEqual(1 + 4, len(calls))
        # first_dataset
        self.assertEqual((), calls[0].args)
        self.assertEqual(dict(path='1', streaming=True), calls[0].kwargs)
        # dsets
        self.assertEqual((), calls[1].args)
        expected_kwargs_1 = dict(
            path='1',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_1, calls[1].kwargs)
        self.assertEqual((), calls[2].args)
        expected_kwargs_2 = dict(
            path='0',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_2, calls[2].kwargs)
        self.assertEqual((), calls[3].args)
        expected_kwargs_3 = dict(
            path='3',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_3, calls[3].kwargs)
        self.assertEqual((), calls[4].args)
        expected_kwargs_4 = dict(
            path='2',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_4, calls[4].kwargs)
        self.assertEqual({'even': 2, 'odd': 3}, next(iterator))
        self.assertEqual({'even': -2, 'odd': -3}, next(iterator))
        self.assertEqual({'even': 0, 'odd': 1}, next(iterator))
        self.assertEqual({'even': 0, 'odd': -1}, next(iterator))
        self.assertEqual({'even': 6, 'odd': 7}, next(iterator))
        self.assertEqual({'even': -6, 'odd': -7}, next(iterator))
        self.assertEqual({'even': 4, 'odd': 5}, next(iterator))
        self.assertEqual({'even': -4, 'odd': -5}, next(iterator))
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_load__skip_not_none__skips_before_loading(self):
        configs = [{'path': '1'}, {'path': '0'}, {'path': '3'}, {'path': '2'}]
        loader = loaders.HuggingFaceMultiLoader(configs, skip=3)
        def do_side_effect(path: str, *args, **kwargs) -> datasets.Dataset:
            i = int(path)
            def generator():
                yield {'even': 2 * i, 'odd': 2 * i + 1}
                yield {'even': - (2 * i), 'odd': - (2 * i + 1)}
            dataset = datasets.Dataset.from_generator(generator)
            return dataset
        with mock.patch('datasets.load_dataset') as mock_load_dataset:
            mock_load_dataset.side_effect = do_side_effect
            iterator = loader.load()
        calls = mock_load_dataset.call_args_list
        self.assertEqual(1 + 4, len(calls))
        # first_dataset
        self.assertEqual((), calls[0].args)
        self.assertEqual(dict(path='1', streaming=True), calls[0].kwargs)
        # dsets
        self.assertEqual((), calls[1].args)
        expected_kwargs_1 = dict(
            path='1',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_1, calls[1].kwargs)
        self.assertEqual((), calls[2].args)
        expected_kwargs_2 = dict(
            path='0',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_2, calls[2].kwargs)
        self.assertEqual((), calls[3].args)
        expected_kwargs_3 = dict(
            path='3',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_3, calls[3].kwargs)
        self.assertEqual((), calls[4].args)
        expected_kwargs_4 = dict(
            path='2',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_4, calls[4].kwargs)
        self.assertEqual({'even': 0, 'odd': -1}, next(iterator))
        self.assertEqual({'even': 6, 'odd': 7}, next(iterator))
        self.assertEqual({'even': -6, 'odd': -7}, next(iterator))
        self.assertEqual({'even': 4, 'odd': 5}, next(iterator))
        self.assertEqual({'even': -4, 'odd': -5}, next(iterator))
        with self.assertRaises(StopIteration):
            next(iterator)

    def test_load__limit_not_none__loads_up_to_limit(self):
        configs = [{'path': '1'}, {'path': '0'}, {'path': '3'}, {'path': '2'}]
        loader = loaders.HuggingFaceMultiLoader(configs, limit=3)
        def do_side_effect(path: str, *args, **kwargs) -> datasets.Dataset:
            i = int(path)
            def generator():
                yield {'even': 2 * i, 'odd': 2 * i + 1}
                yield {'even': - (2 * i), 'odd': - (2 * i + 1)}
            dataset = datasets.Dataset.from_generator(generator)
            return dataset
        with mock.patch('datasets.load_dataset') as mock_load_dataset:
            mock_load_dataset.side_effect = do_side_effect
            iterator = loader.load()
        calls = mock_load_dataset.call_args_list
        self.assertEqual(1 + 4, len(calls))
        # first_dataset
        self.assertEqual((), calls[0].args)
        self.assertEqual(dict(path='1', streaming=True), calls[0].kwargs)
        # dsets
        self.assertEqual((), calls[1].args)
        expected_kwargs_1 = dict(
            path='1',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_1, calls[1].kwargs)
        self.assertEqual((), calls[2].args)
        expected_kwargs_2 = dict(
            path='0',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_2, calls[2].kwargs)
        self.assertEqual((), calls[3].args)
        expected_kwargs_3 = dict(
            path='3',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_3, calls[3].kwargs)
        self.assertEqual((), calls[4].args)
        expected_kwargs_4 = dict(
            path='2',
            streaming=True,
            features=dict(
                even=datasets.Value('int64'),
                odd=datasets.Value('int64'),
            ),
        )
        self.assertEqual(expected_kwargs_4, calls[4].kwargs)
        self.assertEqual({'even': 2, 'odd': 3}, next(iterator))
        self.assertEqual({'even': -2, 'odd': -3}, next(iterator))
        self.assertEqual({'even': 0, 'odd': 1}, next(iterator))
        with self.assertRaises(StopIteration):
            next(iterator)
