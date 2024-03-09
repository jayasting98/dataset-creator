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
        maven_dir_pathname = (
            os.path.join(self._home_dir_pathname, '.m2', 'repository'))
        expected_jar_pathnames = [
            os.path.join(maven_dir_pathname, 'junit', 'junit', '4.11',
                'junit-4.11.jar'),
            os.path.join(maven_dir_pathname, 'org', 'hamcrest', 'hamcrest-core',
                '1.3', 'hamcrest-core-1.3.jar'),
            os.path.join(maven_dir_pathname, 'org', 'mockito', 'mockito-core',
                '3.12.4', 'mockito-core-3.12.4.jar'),
            os.path.join(maven_dir_pathname, 'net', 'bytebuddy', 'byte-buddy',
                '1.11.13', 'byte-buddy-1.11.13.jar'),
            os.path.join(maven_dir_pathname, 'net', 'bytebuddy',
                'byte-buddy-agent', '1.11.13', 'byte-buddy-agent-1.11.13.jar'),
            os.path.join(maven_dir_pathname, 'org', 'objenesis', 'objenesis',
                '3.2', 'objenesis-3.2.jar'),
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


class GradleRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self._repo_dir_pathname = os.path.join('integration_tests',
            'resources', 'repositories', 'gradle', 'guess-the-number')
        self._repo = repositories.GradleRepository(self._repo_dir_pathname)
        self._home_dir_pathname = str(pathlib.Path.home())

    def test_compile__typical_case__compiles(self):
        self._repo.compile()
        build_dir = os.path.join(self._repo_dir_pathname, 'app', 'build')
        self.assertTrue(os.path.isdir(build_dir))

    def test_compile__fails__raises_error(self):
        with tempfile.TemporaryDirectory() as dir:
            repo = repositories.GradleRepository(dir)
            with self.assertRaises(subprocess.CalledProcessError):
                repo.compile()

    def test_find_jar_pathnames__typical_case__finds_correctly(self):
        gradle_dir_pathname = os.path.join(self._home_dir_pathname, '.gradle',
            'caches', 'modules-2', 'files-2.1')
        expected_jar_pathnames = [
            os.path.join(gradle_dir_pathname, 'junit', 'junit', '4.11',
                '4e031bb61df09069aeb2bffb4019e7a5034a4ee0', 'junit-4.11.jar'),
            os.path.join(gradle_dir_pathname, 'org.hamcrest', 'hamcrest-core',
                '1.3', '42a25dc3219429f0e5d060061f71acb49bf010a0',
                'hamcrest-core-1.3.jar'),
            os.path.join(gradle_dir_pathname, 'org.mockito', 'mockito-core',
                '3.12.4', 'f9cdc14ea4a3573c0c0366d47d5ca960be24ddb6',
                'mockito-core-3.12.4.jar'),
            os.path.join(gradle_dir_pathname, 'net.bytebuddy', 'byte-buddy',
                '1.11.13', 'a85d4d74de5ce7a4dd5cbbd337ced6af2740acd',
                'byte-buddy-1.11.13.jar'),
            os.path.join(gradle_dir_pathname, 'net.bytebuddy',
                'byte-buddy-agent', '1.11.13',
                '8c7aaa0ef9863fa89a711bfc5d8e2e0affa0d67f',
                'byte-buddy-agent-1.11.13.jar'),
            os.path.join(gradle_dir_pathname, 'org.objenesis', 'objenesis',
                '3.2', '7fadf57620c8b8abdf7519533e5527367cb51f09',
                'objenesis-3.2.jar'),
        ]
        actual_jar_pathnames = self._repo.find_jar_pathnames()
        self.assertCountEqual(expected_jar_pathnames, actual_jar_pathnames)

    def test_find_focal_classpath__typical_case__finds_correctly(self):
        expected_focal_classpath = os.path.join(os.getcwd(),
            'integration_tests', 'resources', 'repositories', 'gradle',
            'guess-the-number', 'app', 'build', 'classes', 'java', 'main')
        actual_focal_classpath = self._repo.find_focal_classpath()
        self.assertEqual(expected_focal_classpath, actual_focal_classpath)

    def test_find_test_classpath__typical_case__finds_correctly(self):
        expected_test_classpath = os.path.join(os.getcwd(),
            'integration_tests', 'resources', 'repositories', 'gradle',
            'guess-the-number', 'app', 'build', 'classes', 'java', 'test')
        actual_test_classpath = self._repo.find_test_classpath()
        self.assertEqual(expected_test_classpath, actual_test_classpath)


class RepositoriesTest(unittest.TestCase):
    def test_create_repository__maven_repository__creates_correctly(self):
        repo_dir_pathname = os.path.join('integration_tests',
            'resources', 'repositories', 'maven', 'guess-the-number')
        repo = repositories.create_repository(repo_dir_pathname)
        self.assertIsInstance(repo, repositories.MavenRepository)

    def test_create_repository__gradle_repository__creates_correctly(self):
        repo_dir_pathname = os.path.join('integration_tests',
            'resources', 'repositories', 'gradle', 'guess-the-number')
        repo = repositories.create_repository(repo_dir_pathname)
        self.assertIsInstance(repo, repositories.GradleRepository)

    def test_create_repository__unsupported_repo_type__creates_correctly(self):
        with (tempfile.TemporaryDirectory() as dir,
            self.assertRaises(ValueError)):
            repositories.create_repository(dir)
