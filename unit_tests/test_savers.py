import unittest
from unittest import mock

from dataset_creator import savers


class HuggingFaceGoogleCloudStorageSaver(unittest.TestCase):
    def test_save__typical_case__saves(self):
        with mock.patch('gcsfs.GCSFileSystem') as mock_gcsfs:
            saver = savers.HuggingFaceGoogleCloudStorageSaver(
                'project_id', 'bucket_name', 'path/name')
        mock_gcsfs.assert_called_once_with(project='project_id', token=None)
        samples = [{'data': 0}, {'data': 1}, {'data': 2}, {'data': 3}]
        mock_dataset = mock.MagicMock()
        with (mock
            .patch('datasets.Dataset.from_generator') as mock_from_generator):
            mock_from_generator.return_value = mock_dataset
            saver.save(iter(samples))
        mock_from_generator.assert_called_once()
        call = mock_from_generator.call_args
        args = call.args
        self.assertEqual(1, len(args))
        generator = args[0]
        iterator = generator()
        self.assertEqual({'data': 0}, next(iterator))
        self.assertEqual({'data': 1}, next(iterator))
        self.assertEqual({'data': 2}, next(iterator))
        self.assertEqual({'data': 3}, next(iterator))
        with self.assertRaises(StopIteration):
            next(iterator)
        mock_dataset.save_to_disk.assert_called_once_with(
            'gs://bucket_name/path/name',
            storage_options={'project': 'project_id', 'token': None},
        )

    def test_save__with_limit__saves_up_to_limit(self):
        with mock.patch('gcsfs.GCSFileSystem') as mock_gcsfs:
            saver = savers.HuggingFaceGoogleCloudStorageSaver(
                'project_id', 'bucket_name', 'path/name', limit=2)
        mock_gcsfs.assert_called_once_with(project='project_id', token=None)
        samples = [{'data': 0}, {'data': 1}, {'data': 2}, {'data': 3}]
        mock_dataset = mock.MagicMock()
        with (mock
            .patch('datasets.Dataset.from_generator') as mock_from_generator):
            mock_from_generator.return_value = mock_dataset
            saver.save(iter(samples))
        mock_from_generator.assert_called_once()
        call = mock_from_generator.call_args
        args = call.args
        self.assertEqual(1, len(args))
        generator = args[0]
        iterator = generator()
        self.assertEqual({'data': 0}, next(iterator))
        self.assertEqual({'data': 1}, next(iterator))
        with self.assertRaises(StopIteration):
            next(iterator)
        mock_dataset.save_to_disk.assert_called_once_with(
            'gs://bucket_name/path/name',
            storage_options={'project': 'project_id', 'token': None},
        )
