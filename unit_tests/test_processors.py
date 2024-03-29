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
            .TheStackRepositoryProcessor(mock_loader, mock_saver))
        processor.process()
        mock_saver.save.assert_called_once()
        save_call = mock_saver.save.call_args
        save_args = save_call.args
        self.assertEqual(1, len(save_args))
        actual_iterator = save_args[0]
        expected_repository_sample_0 = {'repository_name': 'user1/repo1',
            'repository_url': 'https://github.com/user1/repo1'}
        self.assertEqual(expected_repository_sample_0, next(actual_iterator))
        expected_repository_sample_1 = {'repository_name': 'user1/repo2',
            'repository_url': 'https://github.com/user1/repo2'}
        self.assertEqual(expected_repository_sample_1, next(actual_iterator))
        expected_repository_sample_2 = {'repository_name': 'user2/repo1',
            'repository_url': 'https://github.com/user2/repo1'}
        self.assertEqual(expected_repository_sample_2, next(actual_iterator))
        with self.assertRaises(StopIteration):
            next(actual_iterator)


class IdentityProcessorTest(unittest.TestCase):
    def test_process__typical_data__saves_loaded_data_exactly(self):
        mock_loader = mock.MagicMock()
        dataset = ['Hello', 'World!']
        mock_loader.load.return_value = iter(dataset)
        mock_saver = mock.MagicMock()
        processor = processors.IdentityProcessor(mock_loader, mock_saver)
        processor.process()
        mock_saver.save.assert_called_once()
        save_call = mock_saver.save.call_args
        save_args = save_call.args
        self.assertEqual(1, len(save_args))
        actual_iterator = save_args[0]
        self.assertEqual('Hello', next(actual_iterator))
        self.assertEqual('World!', next(actual_iterator))
        with self.assertRaises(StopIteration):
            next(actual_iterator)


class UniqueCoverageSamplesProcessorTest(unittest.TestCase):
    def test_process__typical_data__takes_samples_and_deduplicates(self):
        mock_loader = mock.MagicMock()
        samples = [
            dict(
                focal_method=dict(
                    body='doA()',
                ),
                test_input_method=dict(
                    body='testDoA_givenAlpha()',
                ),
                test_target_method=dict(
                    body='testDoA_givenBeta()',
                ),
            ),
            dict(
                focal_method=dict(
                    body='doA()',
                ),
                test_input_method=dict(
                    body='testDoA_givenAlpha()',
                ),
                test_target_method=dict(
                    body='testDoA_givenGamma()',
                ),
            ),
            dict(
                focal_method=dict(
                    body='doA()',
                ),
                test_input_method=dict(
                    body='testDoA_givenAlpha()',
                ),
                test_target_method=dict(
                    body='testDoA_givenBeta()',
                ),
            ),
            dict(
                focal_method=dict(
                    body='doB()',
                ),
                test_input_method=dict(
                    body='testDoB_givenBeta()',
                ),
                test_target_method=dict(
                    body='testDoB_givenAlpha()',
                ),
            ),
        ]
        mock_loader.load.return_value = iter(samples)
        mock_saver = mock.MagicMock()
        processor = (processors
            .UniqueCoverageSamplesProcessor(mock_loader, mock_saver))
        processor.process()
        mock_saver.save.assert_called_once()
        save_call = mock_saver.save.call_args
        save_args = save_call.args
        self.assertEqual(1, len(save_args))
        actual_iterator = save_args[0]
        expected_repository_sample_0 = dict(
            focal_method=dict(
                body='doA()',
            ),
            test_input_method=dict(
                body='testDoA_givenAlpha()',
            ),
            test_target_method=dict(
                body='testDoA_givenBeta()',
            ),
        )
        self.assertEqual(expected_repository_sample_0, next(actual_iterator))
        expected_repository_sample_1 = dict(
            focal_method=dict(
                body='doA()',
            ),
            test_input_method=dict(
                body='testDoA_givenAlpha()',
            ),
            test_target_method=dict(
                body='testDoA_givenGamma()',
            ),
        )
        self.assertEqual(expected_repository_sample_1, next(actual_iterator))
        expected_repository_sample_2 = dict(
            focal_method=dict(
                body='doB()',
            ),
            test_input_method=dict(
                body='testDoB_givenBeta()',
            ),
            test_target_method=dict(
                body='testDoB_givenAlpha()',
            ),
        )
        self.assertEqual(expected_repository_sample_2, next(actual_iterator))
        with self.assertRaises(StopIteration):
            next(actual_iterator)
