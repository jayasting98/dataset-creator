import os
import pathlib
import shutil
import unittest

from dataset_creator import savers


class LocalFileSaverTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._test_directory = os.path.join('test_work_dir', 'local_file_saver')
        pathlib.Path(cls._test_directory).mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls._test_directory)

    def test_save__non_existent_file__creates_and_saves(self):
        directory = os.path.join(self.__class__._test_directory, 'save')
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        file_pathname = (os.path.join(directory, 'non_existent.txt'))
        saver = savers.LocalFileSaver(file_pathname)
        samples = ['Hello', 'World!']
        saver.save(samples)
        expected_lines = ['Hello\n', 'World!\n']
        with open(file_pathname) as file:
            actual_lines = file.readlines()
            self.assertEqual(expected_lines, actual_lines)

    def test_save__empty_file__appends_and_saves(self):
        directory = os.path.join(self.__class__._test_directory, 'save', 'dir')
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        file_pathname = (os.path.join(directory, 'empty.txt'))
        open(file_pathname, 'w').close()
        saver = savers.LocalFileSaver(file_pathname)
        samples = ['Hello', 'World!']
        saver.save(samples)
        expected_lines = ['Hello\n', 'World!\n']
        with open(file_pathname) as file:
            actual_lines = file.readlines()
            self.assertEqual(expected_lines, actual_lines)

    def test_save__non_empty_file_with_limit__appends_until_limit(self):
        directory = os.path.join(self.__class__._test_directory, 'save')
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        file_pathname = (os.path.join(directory, 'limit_empty.txt'))
        open(file_pathname, 'w').close()
        saver = savers.LocalFileSaver(file_pathname, limit=1)
        samples = ['Hello', 'World!']
        saver.save(samples)
        expected_lines = ['Hello\n']
        with open(file_pathname) as file:
            actual_lines = file.readlines()
            self.assertEqual(expected_lines, actual_lines)

    def test_save__non_empty_file__appends_and_saves(self):
        directory = os.path.join(self.__class__._test_directory, 'save')
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        file_pathname = (os.path.join(directory, 'non_empty.txt'))
        with open(file_pathname, 'w') as file:
            file.write('Message\n')
        saver = savers.LocalFileSaver(file_pathname)
        samples = ['Hello', 'World!']
        saver.save(samples)
        expected_lines = ['Message\n', 'Hello\n', 'World!\n']
        with open(file_pathname) as file:
            actual_lines = file.readlines()
            self.assertEqual(expected_lines, actual_lines)
