import unittest
from unittest import mock

from dataset_creator import processors


class TheStackRepositoryProcessorTest(unittest.TestCase):
    def test_process__typical_data__takes_repositories_and_deduplicates(self):
        mock_loader = mock.MagicMock()
        data_values = [
            ('user1/repo1', 0),
            ('user1/repo2', 0),
            ('user2/repo1', 0),
            ('user1/repo2', 1),
        ]
        dataset = [{'max_stars_repo_name': repo_name, 'ignored': dummy}
            for repo_name, dummy in data_values]
        mock_loader.load.return_value = iter(dataset)
        mock_saver = mock.MagicMock()
        processor = (processors
            .TheStackRepositoryProcessor(mock_loader, mock_saver, {}))
        processor.process()
        mock_saver.save.assert_called_once()
        save_call = mock_saver.save.call_args
        save_args = save_call.args
        self.assertEqual(1, len(save_args))
        actual_iterator = save_args[0]
        self.assertEqual(
            {'repository_name': 'user1/repo1'}, next(actual_iterator))
        self.assertEqual(
            {'repository_name': 'user1/repo2'}, next(actual_iterator))
        self.assertEqual(
            {'repository_name': 'user2/repo1'}, next(actual_iterator))
        with self.assertRaises(StopIteration):
            next(actual_iterator)
