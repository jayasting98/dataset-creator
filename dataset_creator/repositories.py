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


class GradleRepository(Repository):
    def __init__(self: Self, root_dir_pathname: str) -> None:
        self._root_dir_pathname = root_dir_pathname

    def compile(self: Self) -> None:
        return super().compile()

    def find_jar_pathnames(self: Self) -> list[str]:
        return super().find_jar_pathnames()

    def find_focal_classpath(self: Self) -> str:
        return super().find_focal_classpath()

    def find_test_classpath(self: Self) -> str:
        return super().find_test_classpath()
