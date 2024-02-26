import unittest
from unittest import mock

import datasets

from dataset_creator import loaders
from dataset_creator import processors
from dataset_creator import savers


class TheStackRepositoryProcessorTest(unittest.TestCase):
    def test_process__hugging_face_to_google_cloud_storage__loads_then_saves(
        self,
    ):
        data_values = [
            ('user1/repo1', 0),
            ('user1/repo2', 0),
            ('user2/repo1', 0),
            ('user1/repo2', 1),
        ]
        samples = [{'max_stars_repo_name': repo_name, 'ignored': dummy}
            for repo_name, dummy in data_values]
        def generator():
            for sample in samples:
                yield sample
        loader = loaders.HuggingFaceLoader(dict())
        saver = savers.HuggingFaceGoogleCloudStorageSaver(
            'project_id', 'bucket_name', 'path/name')
        processor = (processors
            .TheStackRepositoryProcessor(loader, saver))
        with (
            mock.patch('datasets.load_dataset') as mock_load_dataset,
            mock.patch('datasets.Dataset.save_to_disk') as mock_save_to_disk,
        ):
            mock_load_dataset.return_value = (
                datasets.Dataset.from_generator(generator))
            processor.process()
        mock_load_dataset.assert_called_once_with(streaming=True)
        mock_save_to_disk.assert_called_once_with(
            'gs://bucket_name/path/name',
            storage_options={'project': 'project_id'},
        )
