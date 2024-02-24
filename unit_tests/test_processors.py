import unittest
from unittest import mock

import datasets

from dataset_creator import processors


class TheStackRepositoryProcessorTest(unittest.TestCase):
    def test_process__typical_data__takes_repositories_and_deduplicates(self):
        mock_loader = mock.MagicMock()
        mapping = {
            'max_stars_repo_name': [
                'user1/repo1', 'user1/repo2', 'user2/repo1', 'user1/repo2'],
            'ignored': [0, 1, 2, 3],
        }
        mock_loader.load.return_value = (datasets
            .Dataset.from_dict(mapping).to_iterable_dataset())
        mock_saver = mock.MagicMock()
        processor = (processors
            .TheStackRepositoryProcessor(mock_loader, mock_saver, {}))
        processor.process()
        mock_saver.save.assert_called_once()
        save_call = mock_saver.save.call_args
        save_args = save_call.args
        self.assertEqual(1, len(save_args))
        actual_ds = save_args[0]
        actual_it = iter(actual_ds)
        self.assertEqual(
            {'max_stars_repo_name': 'user1/repo1'}, next(actual_it))
        self.assertEqual(
            {'max_stars_repo_name': 'user1/repo2'}, next(actual_it))
        self.assertEqual(
            {'max_stars_repo_name': 'user2/repo1'}, next(actual_it))
        with self.assertRaises(StopIteration):
            next(actual_it)
