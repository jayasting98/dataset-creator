import os
import pathlib
import shutil
import unittest

from dataset_creator import savers


class TextSaverTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._test_directory = os.path.join('tests', 'text_saver')
        pathlib.Path(cls._test_directory).mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls._test_directory)

    def test_save__non_existent_file__creates_and_saves(self):
        directory = os.path.join(self.__class__._test_directory, 'save')
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        file_pathname = (os.path.join(directory, 'non_existent.txt'))
        config = {'file_pathname': file_pathname}
        saver = savers.TextSaver(config)
        samples = ['Hello', 'World!']
        saver.save(samples)
        with open(file_pathname) as file:
            lines = file.readlines()
            self.assertEqual('Hello\n', lines[0])
            self.assertEqual('World!\n', lines[1])

    def test_save__empty_file__appends_and_saves(self):
        directory = os.path.join(self.__class__._test_directory, 'save')
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        file_pathname = (os.path.join(directory, 'empty.txt'))
        open(file_pathname, 'w').close()
        config = {'file_pathname': file_pathname}
        saver = savers.TextSaver(config)
        samples = ['Hello', 'World!']
        saver.save(samples)
        with open(file_pathname) as file:
            lines = file.readlines()
            self.assertEqual('Hello\n', lines[0])
            self.assertEqual('World!\n', lines[1])

    def test_save__non_empty_file__appends_and_saves(self):
        directory = os.path.join(self.__class__._test_directory, 'save')
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        file_pathname = (os.path.join(directory, 'non_empty.txt'))
        with open(file_pathname, 'w') as file:
            file.write('Message\n')
        config = {'file_pathname': file_pathname}
        saver = savers.TextSaver(config)
        samples = ['Hello', 'World!']
        saver.save(samples)
        with open(file_pathname) as file:
            lines = file.readlines()
            self.assertEqual('Message\n', lines[0])
            self.assertEqual('Hello\n', lines[1])
            self.assertEqual('World!\n', lines[2])
