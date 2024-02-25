import json
import os
import pathlib
import shutil
import unittest
from unittest import mock

import datasets

from dataset_creator import argument_parsers
from dataset_creator import main


class MainTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._test_directory = os.path.join('test_work_dir', 'main')
        pathlib.Path(cls._test_directory).mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls._test_directory)

    def test_main__typical_case__creates_dataset(self):
        config_file_pathname = (
            os.path.join(self.__class__._test_directory, 'typical.json'))
        save_file_pathname = (
            os.path.join(self.__class__._test_directory, 'typical.out'))
        config = {'loader': {}, 'saver': {'file_pathname': save_file_pathname}}
        with open(config_file_pathname, mode='w') as config_file:
            json.dump(config, config_file)
        def generator():
            yield {'ignore': 'me', 'max_stars_repo_name': 'user1/repo1'}
            yield {'ignore': 'me', 'max_stars_repo_name': 'user1/repo2'}
            yield {'ignore': 'me', 'max_stars_repo_name': 'user2/repo1'}
            yield {'ignore': 'me too', 'max_stars_repo_name': 'user1/repo2'}
        dataset = datasets.Dataset.from_generator(generator)
        parser = argument_parsers.create_parser()
        args = parser.parse_args(
            ['--creator', 'stack_local', '--config_path', config_file_pathname])
        with mock.patch('datasets.load_dataset') as mock_load_dataset:
            mock_load_dataset.return_value = dataset
            main.main(args)
        with open(save_file_pathname) as file:
            lines = file.readlines()
            self.assertEqual(
                "{'repository_name': 'user1/repo1'}\n", lines[0])
            self.assertEqual(
                "{'repository_name': 'user1/repo2'}\n", lines[1])
            self.assertEqual(
                "{'repository_name': 'user2/repo1'}\n", lines[2])
