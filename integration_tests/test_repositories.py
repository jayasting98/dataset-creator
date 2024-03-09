import os
import pathlib
import subprocess
import tempfile
import unittest

from dataset_creator import repositories


class MavenRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self._repo_dir_pathname = os.path.join('integration_tests',
            'resources', 'repositories', 'maven', 'guess-the-number')
        self._repo = repositories.MavenRepository(self._repo_dir_pathname)
        self._home_dir_pathname = str(pathlib.Path.home())

    def test_compile__typical_case__compiles(self):
        self._repo.compile()
        build_dir = os.path.join(self._repo_dir_pathname, 'target')
        self.assertTrue(os.path.isdir(build_dir))

    def test_compile__fails__raises_error(self):
        with tempfile.TemporaryDirectory() as dir:
            repo = repositories.MavenRepository(dir)
            with self.assertRaises(subprocess.CalledProcessError):
                repo.compile()

    def test_find_jar_pathnames__typical_case__finds_jar_pathnames(self):
        expected_jar_pathnames = [
            os.path.join(self._home_dir_pathname, '.m2', 'repository', 'junit',
                'junit', '4.11', 'junit-4.11.jar'),
            os.path.join(self._home_dir_pathname, '.m2', 'repository', 'org',
                'hamcrest', 'hamcrest-core', '1.3', 'hamcrest-core-1.3.jar'),
            os.path.join(self._home_dir_pathname, '.m2', 'repository', 'org',
                'mockito', 'mockito-core', '3.12.4', 'mockito-core-3.12.4.jar'),
            os.path.join(self._home_dir_pathname, '.m2', 'repository', 'net',
                'bytebuddy', 'byte-buddy', '1.11.13', 'byte-buddy-1.11.13.jar'),
            os.path.join(self._home_dir_pathname, '.m2', 'repository', 'net',
                'bytebuddy', 'byte-buddy-agent', '1.11.13',
                'byte-buddy-agent-1.11.13.jar'),
            os.path.join(self._home_dir_pathname, '.m2', 'repository', 'org',
                'objenesis', 'objenesis', '3.2', 'objenesis-3.2.jar'),
        ]
        actual_jar_pathnames = self._repo.find_jar_pathnames()
        self.assertCountEqual(expected_jar_pathnames, actual_jar_pathnames)

    def test_find_focal_classpath__typical_case__finds_correctly(self):
        expected_focal_classpath = os.path.join(os.getcwd(),
            'integration_tests', 'resources', 'repositories', 'maven',
            'guess-the-number', 'target', 'classes')
        actual_focal_classpath = self._repo.find_focal_classpath()
        self.assertEqual(expected_focal_classpath, actual_focal_classpath)

    def test_find_test_classpath__typical_case__finds_correctly(self):
        expected_test_classpath = os.path.join(os.getcwd(),
            'integration_tests', 'resources', 'repositories', 'maven',
            'guess-the-number', 'target', 'test-classes')
        actual_test_classpath = self._repo.find_test_classpath()
        self.assertEqual(expected_test_classpath, actual_test_classpath)
