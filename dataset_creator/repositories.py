import abc
import glob
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
        jar_pathnames = output.split(os.pathsep)
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

    def _find_test_classpath(self: Self) -> str:
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

def create_repository(root_dir_pathname: str) -> Repository:
    if os.path.isfile(os.path.join(root_dir_pathname, 'pom.xml')):
        return MavenRepository(root_dir_pathname)
    if (os.path.isfile(os.path.join(root_dir_pathname, 'build.gradle'))
        or os.path.isfile(os.path.join(root_dir_pathname, 'build.gradle.kts'))):
        return GradleRepository(root_dir_pathname)
    possible_build_gradle_pathnames = (glob
        .glob('**/build.gradle', recursive=True, root_dir=root_dir_pathname))
    possible_build_gradle_pathnames.extend(glob.glob(
        '**/build.gradle.kts', recursive=True, root_dir=root_dir_pathname))
    for file_pathname in possible_build_gradle_pathnames:
        if os.path.isfile(file_pathname):
            return GradleRepository(root_dir_pathname)
    raise ValueError()
