import abc
import os
import subprocess
from typing import Self

from dataset_creator import utilities


class Repository(abc.ABC):
    @abc.abstractmethod
    def compile(self: Self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_jar_pathnames(self: Self) -> list[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_focal_classpath(self: Self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_test_classpath(self: Self) -> str:
        raise NotImplementedError()


class MavenRepository(Repository):
    def __init__(self: Self, root_dir_pathname: str) -> None:
        self._root_dir_pathname = root_dir_pathname

    def compile(self: Self) -> None:
        args = ['mvn', 'clean', 'test-compile']
        with utilities.WorkingDirectory(self._root_dir_pathname):
            completed_process = subprocess.run(args, stdout=subprocess.DEVNULL)
        completed_process.check_returncode()

    def find_jar_pathnames(self: Self) -> list[str]:
        args = ['mvn', 'dependency:build-classpath',
            '-Dmdep.outputFile=/dev/stdout', '-q']
        with utilities.WorkingDirectory(self._root_dir_pathname):
            completed_process = (
                subprocess.run(args, capture_output=True, text=True))
        completed_process.check_returncode()
        output = completed_process.stdout
        jar_pathnames = output.split(':')
        return jar_pathnames

    def find_focal_classpath(self: Self) -> str:
        args = ['mvn', 'help:evaluate',
            '-Dexpression=project.build.outputDirectory', '-q', '-DforceStdout']
        with utilities.WorkingDirectory(self._root_dir_pathname):
            completed_process = (
                subprocess.run(args, capture_output=True, text=True))
        completed_process.check_returncode()
        focal_classpath = completed_process.stdout
        return focal_classpath

    def find_test_classpath(self: Self) -> str:
        args = ['mvn', 'help:evaluate',
            '-Dexpression=project.build.testOutputDirectory', '-q',
            '-DforceStdout']
        with utilities.WorkingDirectory(self._root_dir_pathname):
            completed_process = (
                subprocess.run(args, capture_output=True, text=True))
        completed_process.check_returncode()
        test_classpath = completed_process.stdout
        return test_classpath


_gradle_init_script_pathname = (
    os.path.join(os.getcwd(), 'scripts', 'init.gradle.kts'))


class GradleRepository(Repository):
    def __init__(self: Self, root_dir_pathname: str) -> None:
        self._root_dir_pathname = root_dir_pathname
        self._init_script_rel_pathname = (os.path
            .relpath(_gradle_init_script_pathname, self._root_dir_pathname))

    def compile(self: Self) -> None:
        args = ['gradle', 'clean', 'testClasses']
        with utilities.WorkingDirectory(self._root_dir_pathname):
            completed_process = subprocess.run(
                args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        completed_process.check_returncode()

    def find_jar_pathnames(self: Self) -> list[str]:
        project_name = self._find_project_name()
        args = ['gradle', '-q', '--init-script', self._init_script_rel_pathname,
            f'{project_name}:buildTestRuntimeClasspath']
        with utilities.WorkingDirectory(self._root_dir_pathname):
            completed_process = (
                subprocess.run(args, capture_output=True, text=True))
        completed_process.check_returncode()
        output = completed_process.stdout
        line = output.split(os.linesep)[0]
        classpath_pathnames = line.split(os.pathsep)
        jar_pathnames = [pathname
            for pathname in classpath_pathnames if pathname.endswith('.jar')]
        return jar_pathnames

    def find_focal_classpath(self: Self) -> str:
        project_name = self._find_project_name()
        args = ['gradle', '-q', '--init-script', self._init_script_rel_pathname,
            f'{project_name}:buildTestRuntimeClasspath']
        with utilities.WorkingDirectory(self._root_dir_pathname):
            completed_process = (
                subprocess.run(args, capture_output=True, text=True))
        completed_process.check_returncode()
        output = completed_process.stdout
        line = output.split(os.linesep)[0]
        classpath_pathnames = line.split(os.pathsep)
        candidates = [pathname for pathname in classpath_pathnames
            if 'main' in pathname and 'classes' in pathname]
        focal_classpath = candidates[0]
        return focal_classpath

    def find_test_classpath(self: Self) -> str:
        project_name = self._find_project_name()
        args = ['gradle', '-q', '--init-script', self._init_script_rel_pathname,
            f'{project_name}:buildTestRuntimeClasspath']
        with utilities.WorkingDirectory(self._root_dir_pathname):
            completed_process = (
                subprocess.run(args, capture_output=True, text=True))
        completed_process.check_returncode()
        output = completed_process.stdout
        line = output.split(os.linesep)[0]
        classpath_pathnames = line.split(os.pathsep)
        candidates = [pathname for pathname in classpath_pathnames
            if 'test' in pathname and 'classes' in pathname]
        test_classpath = candidates[0]
        return test_classpath

    def _find_project_name(self: Self) -> str:
        try:
            return self._project_name
        except AttributeError:
            args = ['gradle', '-q',
                '--init-script', self._init_script_rel_pathname,
                ':listSubprojects']
            with utilities.WorkingDirectory(self._root_dir_pathname):
                completed_process = (
                    subprocess.run(args, capture_output=True, text=True))
            completed_process.check_returncode()
            output = completed_process.stdout
            project_names = output.split(os.linesep)
            self._project_name = project_names[0]
            return self._project_name
