import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest

from dataset_creator import projects


class MavenProjectTest(unittest.TestCase):
    def setUp(self) -> None:
        self._root_dir_pathname = os.path.join(os.getcwd(), 'integration_tests',
            'resources', 'repositories', 'maven', 'guess-the-number')
        self._proj_dir_pathname = os.path.join(os.getcwd(), 'integration_tests',
            'resources', 'repositories', 'maven', 'guess-the-number')
        self._proj = (projects
            .MavenProject(self._root_dir_pathname, self._proj_dir_pathname))
        self._home_dir_pathname = str(pathlib.Path.home())

    def test_find_subproject_pathnames__has_subprojects__finds_correctly(self):
        parent_proj_dir_pathname = os.path.join(os.getcwd(),
            'integration_tests', 'resources', 'repositories', 'maven',
            'parent-project')
        parent_proj = (projects
            .MavenProject(parent_proj_dir_pathname, parent_proj_dir_pathname))
        expected_subproject_pathnames = [
            os.path.join(parent_proj_dir_pathname),
            os.path.join(parent_proj_dir_pathname, 'project'),
            os.path.join(parent_proj_dir_pathname, 'subproject1'),
            os.path.join(parent_proj_dir_pathname, 'project', 'subproject0'),
        ]
        actual_subproject_pathnames = parent_proj.find_subproject_pathnames()
        self.assertEqual(
            expected_subproject_pathnames, actual_subproject_pathnames)

    def test_find_subproject_pathnames__no_subprojects__finds_correctly(self):
        expected_subproject_pathnames = [self._root_dir_pathname]
        actual_subproject_pathnames = self._proj.find_subproject_pathnames()
        self.assertEqual(
            expected_subproject_pathnames, actual_subproject_pathnames)

    def test_compile__typical_case__compiles(self):
        build_dir = os.path.join(self._proj_dir_pathname, 'target')
        if os.path.exists(build_dir) and os.path.isdir(build_dir):
            shutil.rmtree(build_dir)
        self._proj.compile()
        self.assertTrue(os.path.isdir(build_dir))

    def test_compile__fails__raises_error(self):
        with tempfile.TemporaryDirectory() as dir:
            proj = projects.MavenProject(dir, dir)
            with self.assertRaises(subprocess.CalledProcessError):
                proj.compile()

    def test_find_classpath_pathnames__typical_case__finds_correctly(self):
        maven_dir_pathname = (
            os.path.join(self._home_dir_pathname, '.m2', 'repository'))
        expected_classpath_pathnames = [
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
            (os.path.join(self._proj_dir_pathname, 'target', 'classes')
                + os.path.sep),
            (os.path.join(self._proj_dir_pathname, 'target', 'test-classes')
                + os.path.sep),
            (os.path.join(self._proj_dir_pathname, 'src', 'main', 'resources')
                + os.path.sep),
            (os.path.join(self._proj_dir_pathname, 'src', 'test', 'resources')
                + os.path.sep),
        ]
        actual_classpath_pathnames = self._proj.find_classpath_pathnames()
        self.assertCountEqual(
            expected_classpath_pathnames, actual_classpath_pathnames)

    def test_find_focal_classpath__typical_case__finds_correctly(self):
        expected_focal_classpath = os.path.join(os.getcwd(),
            'integration_tests', 'resources', 'repositories', 'maven',
            'guess-the-number', 'target', 'classes', '')
        actual_focal_classpath = self._proj.find_focal_classpath()
        self.assertEqual(expected_focal_classpath, actual_focal_classpath)


class GradleProjectTest(unittest.TestCase):
    def setUp(self) -> None:
        self._root_dir_pathname = os.path.join(os.getcwd(), 'integration_tests',
            'resources', 'repositories', 'gradle', 'guess-the-number')
        self._proj_dir_pathname = os.path.join(os.getcwd(), 'integration_tests',
            'resources', 'repositories', 'gradle', 'guess-the-number', 'app')
        self._proj = (projects
            .GradleProject(self._root_dir_pathname, self._proj_dir_pathname))
        self._home_dir_pathname = str(pathlib.Path.home())

    def test_find_subproject_pathnames__has_subprojects__finds_correctly(self):
        parent_proj_dir_pathname = os.path.join(os.getcwd(),
            'integration_tests', 'resources', 'repositories', 'gradle',
            'parent-project')
        parent_proj = (projects
            .GradleProject(parent_proj_dir_pathname, parent_proj_dir_pathname))
        expected_subproject_pathnames = [
            os.path.join(parent_proj_dir_pathname),
            os.path.join(parent_proj_dir_pathname, 'app'),
            os.path.join(parent_proj_dir_pathname, 'list'),
            os.path.join(parent_proj_dir_pathname, 'project'),
            os.path.join(parent_proj_dir_pathname, 'utilities'),
            os.path.join(parent_proj_dir_pathname, 'project', 'subproject'),
        ]
        actual_subproject_pathnames = parent_proj.find_subproject_pathnames()
        self.assertEqual(
            expected_subproject_pathnames, actual_subproject_pathnames)

    def test_find_subproject_pathnames__no_subprojects__finds_correctly(self):
        parent_proj_dir_pathname = os.path.join(os.getcwd(),
            'integration_tests', 'resources', 'repositories', 'gradle',
            'simple-project')
        parent_proj = (projects
            .GradleProject(parent_proj_dir_pathname, parent_proj_dir_pathname))
        expected_subproject_pathnames = [parent_proj_dir_pathname]
        actual_subproject_pathnames = parent_proj.find_subproject_pathnames()
        self.assertEqual(
            expected_subproject_pathnames, actual_subproject_pathnames)

    def test_compile__typical_case__compiles(self):
        build_dir = os.path.join(self._proj_dir_pathname, 'build')
        if os.path.exists(build_dir) and os.path.isdir(build_dir):
            shutil.rmtree(build_dir)
        self._proj.compile()
        self.assertTrue(os.path.isdir(build_dir))

    def test_compile__fails__raises_error(self):
        with tempfile.TemporaryDirectory() as dir:
            proj = projects.GradleProject(dir, dir)
            with self.assertRaises(subprocess.CalledProcessError):
                proj.compile()

    def test_find_classpath_pathnames__typical_case__finds_correctly(self):
        gradle_dir_pathname = os.path.join(self._home_dir_pathname, '.gradle',
            'caches', 'modules-2', 'files-2.1')
        expected_classpath_pathnames = [
            os.path.join(self._proj_dir_pathname, 'build', 'classes',
                'java', 'main') + os.path.sep,
            os.path.join(self._proj_dir_pathname, 'build', 'classes',
                'java', 'test') + os.path.sep,
            os.path.join(self._proj_dir_pathname, 'build', 'resources',
                'main') + os.path.sep,
            os.path.join(self._proj_dir_pathname, 'build', 'resources',
                'test') + os.path.sep,
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
        actual_classpath_pathnames = self._proj.find_classpath_pathnames()
        self.assertCountEqual(
            expected_classpath_pathnames, actual_classpath_pathnames)

    def test_find_focal_classpath__typical_case__finds_correctly(self):
        expected_focal_classpath = os.path.join(os.getcwd(),
            'integration_tests', 'resources', 'repositories', 'gradle',
            'guess-the-number', 'app', 'build', 'classes', 'java', 'main', '')
        actual_focal_classpath = self._proj.find_focal_classpath()
        self.assertEqual(expected_focal_classpath, actual_focal_classpath)


class ProjectsTest(unittest.TestCase):
    def test_create_project__maven_project__creates_correctly(self):
        root_dir_pathname = os.path.join('integration_tests',
            'resources', 'repositories', 'maven', 'guess-the-number')
        proj_dir_pathname = root_dir_pathname
        proj = projects.create_project(root_dir_pathname, proj_dir_pathname)
        self.assertIsInstance(proj, projects.MavenProject)

    def test_create_project__gradle_project__creates_correctly(self):
        root_dir_pathname = os.path.join('integration_tests',
            'resources', 'repositories', 'gradle', 'guess-the-number')
        proj_dir_pathname = root_dir_pathname
        proj = projects.create_project(root_dir_pathname, proj_dir_pathname)
        self.assertIsInstance(proj, projects.GradleProject)

    def test_create_project__unsupported_project_type__creates_correctly(self):
        with (tempfile.TemporaryDirectory() as dir,
            self.assertRaises(ValueError)):
            projects.create_project(dir, dir)
