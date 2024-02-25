import unittest
from unittest import mock

from dataset_creator import savers


class HuggingFaceGoogleCloudStorageSaver(unittest.TestCase):
    def test_save__typical_case__saves(self):
        with mock.patch('gcsfs.GCSFileSystem') as mock_gcsfs:
            saver = savers.HuggingFaceGoogleCloudStorageSaver(
                'project_id', 'bucket_name', 'path/name')
        mock_gcsfs.assert_called_once_with(project='project_id')
        samples = [{'data': 0}, {'data': 1}, {'data': 2}, {'data': 3}]
        with mock.patch('datasets.Dataset.save_to_disk') as mock_save_to_disk:
            saver.save(iter(samples))
        mock_save_to_disk.assert_called_once_with(
            'gs://bucket_name/path/name',
            storage_options={'project': 'project_id'},
        )
