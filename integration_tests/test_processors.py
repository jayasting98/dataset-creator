import json
import os
from types import TracebackType
from typing import Any
from typing import Iterator
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
import unittest
from unittest import mock

import datasets
import requests

from dataset_creator import coverages
from dataset_creator import loaders
from dataset_creator import processors
from dataset_creator import savers
from dataset_creator.methods2test import code_parsers


class _MemoryLoader(loaders.Loader[Any]):
    def __init__(self: Self, samples: list[Any]) -> None:
        self._samples = samples

    def load(self: Self) -> loaders.Iterator[Any]:
        iterator = iter(self._samples)
        return iterator


class _MemorySaver(savers.Saver[Any]):
    def save(self: Self, samples: Iterator[Any]) -> None:
        self.samples = list(samples)


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
            storage_options={'project': 'project_id', 'token': None},
        )


class StubTemporaryDirectory:
    def __init__(self: Self, dir_pathname: str) -> None:
        self._dir_pathname = dir_pathname

    def __enter__(self: Self) -> str:
        return self._dir_pathname

    def __exit__(
        self: Self,
        exception_type: type[BaseException],
        exception_value: BaseException,
        exception_traceback: TracebackType,
    ) -> bool:
        return False


class CoverageSamplesProcessorTest(unittest.TestCase):
    def setUp(self) -> None:
        session = requests.Session()
        base_url = 'http://localhost:8080'
        self._code_cov_api = coverages.CodeCovApi(session, base_url)
        script_file_pathname = (
            os.path.join(os.getcwd(), 'code-cov-cli', 'bin', 'code-cov-cli'))
        self._code_cov_cli = (
            coverages.CodeCovCli(script_file_pathname, timeout=10))
        self._parser_type = code_parsers.CodeParser
        self._parser_args = ('java-grammar.so', 'java')

    def _test_process__memory_to_memory__processes_correctly(self, code_cov):
        repo_dir_pathname = os.path.join(os.getcwd(), 'integration_tests',
            'resources', 'repositories', 'maven', 'guess-the-number')
        samples_file_pathname = os.path.join('integration_tests', 'resources',
            'expected_coverage_samples', 'maven', 'guess-the-number',
            'typical_case.json')
        mock_repo = mock.MagicMock()
        mock_repo.head.commit.hexsha = 'hexsha'
        samples = [
            {'repository_url': 'https://github.com/username/guess-the-number'}]
        loader = _MemoryLoader(samples)
        saver = _MemorySaver()
        processor = processors.CoverageSamplesProcessor(loader, saver, code_cov,
            self._parser_type, self._parser_args)
        with open(samples_file_pathname) as samples_file:
            expected_samples = json.load(samples_file)
        with (mock.patch('tempfile.TemporaryDirectory') as mock_temp_dir,
            mock.patch('git.Repo.clone_from') as mock_clone_from):
            mock_temp_dir.return_value = (
                StubTemporaryDirectory(repo_dir_pathname))
            mock_clone_from.return_value = mock_repo
            processor.process()
        actual_samples = saver.samples
        self.assertEqual(expected_samples, actual_samples)

    def _test_process__hugging_face_to_google_cloud_storage__loads_then_saves(
        self, code_cov):
        repo_dir_pathname = os.path.join(os.getcwd(), 'integration_tests',
            'resources', 'repositories', 'maven', 'guess-the-number')
        mock_repo = mock.MagicMock()
        mock_repo.head.commit.hexsha = 'hexsha'
        samples = [
            {'repository_url': 'https://github.com/username/guess-the-number'}]
        def generator():
            for sample in samples:
                yield sample
        loader = loaders.HuggingFaceLoader(dict())
        saver = savers.HuggingFaceGoogleCloudStorageSaver(
            'project_id', 'bucket_name', 'path/name')
        processor = processors.CoverageSamplesProcessor(loader, saver, code_cov,
            self._parser_type, self._parser_args)
        with (
            mock.patch('datasets.load_dataset') as mock_load_dataset,
            mock.patch('tempfile.TemporaryDirectory') as mock_temp_dir,
            mock.patch('git.Repo.clone_from') as mock_clone_from,
            mock.patch('datasets.Dataset.save_to_disk') as mock_save_to_disk,
        ):
            mock_load_dataset.return_value = (
                datasets.Dataset.from_generator(generator))
            mock_temp_dir.return_value = (
                StubTemporaryDirectory(repo_dir_pathname))
            mock_clone_from.return_value = mock_repo
            processor.process()
        mock_load_dataset.assert_called_once_with(streaming=True)
        mock_save_to_disk.assert_called_once_with(
            'gs://bucket_name/path/name',
            storage_options={'project': 'project_id', 'token': None},
        )

    def test_process__code_cov_api_memory_to_memory__processes_correctly(self):
        self._test_process__memory_to_memory__processes_correctly(
            self._code_cov_api)

    def test_process__code_cov_api_hf_to_gcs__loads_then_saves(self):
        self._test_process__memory_to_memory__processes_correctly(
            self._code_cov_api)

    def test_process__code_cov_cli_memory_to_memory__processes_correctly(self):
        self._test_process__memory_to_memory__processes_correctly(
            self._code_cov_cli)

    def test_process__code_cov_cli_hf_to_gcs__loads_then_saves(self):
        self._test_process__memory_to_memory__processes_correctly(
            self._code_cov_cli)
