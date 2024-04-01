import abc
import copy
import logging
import tempfile
import traceback
from typing import Any
from typing import Generator
from typing import Generic
from typing import Iterator
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
from typing import TypeVar

import git

from dataset_creator import coverages
from dataset_creator import loaders
from dataset_creator import projects
from dataset_creator import savers
from dataset_creator import utilities
from dataset_creator.methods2test import code_parsers
from dataset_creator.methods2test import find_map_test_cases


_T = TypeVar('_T')
_U = TypeVar('_U')


class Processor(abc.ABC, Generic[_T, _U]):
    @abc.abstractmethod
    def process(self: Self) -> None:
        raise NotImplementedError()


class TheStackRepositoryProcessor(Processor[dict[str, Any], dict[str, str]]):
    def __init__(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, str]],
    ) -> None:
        self._loader = loader
        self._saver = saver
        self._unique_repository_names = set()

    def process(self: Self) -> None:
        samples = self._loader.load()
        def create_generator():
            for i, sample in enumerate(samples):
                logging.info(f'sample {i}')
                repository_name = sample['max_stars_repo_name']
                if not self._is_unique(repository_name):
                    continue
                repository_sample = dict(
                    repository_name=repository_name,
                    repository_url=f'https://github.com/{repository_name}',
                )
                yield repository_sample
        iterator = utilities.GeneratorFunctionIterator(create_generator)
        self._saver.save(iterator)

    def _is_unique(self: Self, repository_name: str) -> bool:
        if repository_name in self._unique_repository_names:
            return False
        self._unique_repository_names.add(repository_name)
        return True


class IdentityProcessor(Processor[_T, _T]):
    def __init__(
        self: Self,
        loader: loaders.Loader[_T],
        saver: savers.Saver[_T],
    ) -> None:
        self._loader = loader
        self._saver = saver

    def process(self: Self) -> None:
        iterator = self._loader.load()
        self._saver.save(iterator)


class CoverageSamplesProcessor(Processor[dict[str, Any], dict[str, Any]]):
    def __init__(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, Any]],
        code_cov: coverages.CodeCov,
        parser_type: type[code_parsers.CodeParser],
        parser_args: tuple[str, str],
    ) -> None:
        self._loader = loader
        self._saver = saver
        self._code_cov = code_cov
        # Lazy instantiation allows it to pickle the parser (then the iterator).
        self._parser_type = parser_type
        self._parser_args = parser_args

    def process(self: Self) -> None:
        repository_samples = self._loader.load()
        def create_generator():
            for sample in self._create_sample_generator(repository_samples):
                yield sample
        iterator = utilities.GeneratorFunctionIterator(create_generator)
        self._saver.save(iterator)

    @property
    def parser(self: Self) -> code_parsers.CodeParser:
        try:
            return self._parser
        except AttributeError:
            self._parser = self._parser_type(*self._parser_args)
            return self._parser

    def _create_sample_generator(
        self: Self,
        repository_samples: Iterator[dict[str, Any]],
    ) -> Generator[dict[str, Any], None, None]:
        for with_coverage_focal_method_data in (
            self._create_with_coverage_focal_method_data_generator(
                repository_samples)):
            repository_index: int = (
                with_coverage_focal_method_data['repository_index'])
            with_coverage_focal_method_sample = (
                with_coverage_focal_method_data[
                    'with_coverage_focal_method_sample'])
            repository_url = with_coverage_focal_method_data['repository_url']
            repository_hexsha = (
                with_coverage_focal_method_data['repository_hexsha'])
            logging.info(f'repository {repository_index}: generating samples')
            for sample in self._generate_samples(repository_url,
                repository_hexsha, with_coverage_focal_method_sample):
                yield sample

    def _create_with_coverage_focal_method_data_generator(
        self: Self,
        repository_samples: Iterator[dict[str, Any]],
    ) -> Generator[dict[str, Any], None, None]:
        for focal_method_data in (
            self._create_focal_method_data_generator(repository_samples)):
            repository_index: int = focal_method_data['repository_index']
            project_pathname: str = focal_method_data['project_pathname']
            focal_method_sample = focal_method_data['focal_method_sample']
            classpath_pathnames = focal_method_data['classpath_pathnames']
            focal_classpath = focal_method_data['focal_classpath']
            logging.info(f'repository {repository_index}: adding coverage data')
            with_coverage_focal_method_sample = self._add_coverage_data(
                focal_method_sample, classpath_pathnames, focal_classpath,
                project_pathname)
            with_coverage_focal_method_data = {
                'repository_index': repository_index,
                'repository_url': focal_method_data['repository_url'],
                'repository_hexsha': focal_method_data['repository_hexsha'],
                'with_coverage_focal_method_sample':
                    with_coverage_focal_method_sample,
            }
            yield with_coverage_focal_method_data

    def _create_focal_method_data_generator(
        self: Self,
        repository_samples: Iterator[dict[str, Any]],
    ) -> Generator[dict[str, Any], None, None]:
        for project_data in (
            self._create_project_data_generator(repository_samples)):
            repository_index: int = project_data['repository_index']
            root_pathname: str = project_data['root_pathname']
            project_pathname: str = project_data['project_pathname']
            logging.info(f'project dir: {project_pathname}')
            try:
                project = (
                    projects.create_project(root_pathname, project_pathname))
                logging.info(f'repository {repository_index}: compiling')
                project.compile()
                logging.info(
                    f'repository {repository_index}: finding classpath')
                classpath_pathnames = project.find_classpath_pathnames()
                logging.info(
                    f'repository {repository_index}: finding focal classpath')
                focal_classpath = project.find_focal_classpath()
                logging.info(
                    f'repository {repository_index}: '
                    + 'finding focal method samples')
                focal_method_samples = (find_map_test_cases
                    .find_focal_method_samples(
                        project.project_dir_pathname, self.parser))
            except Exception as exception:
                logging.warn(f'repository {repository_index}: {exception}')
                logging.debug(f'{traceback.format_exc()}')
                continue
            for focal_method_sample in focal_method_samples:
                focal_method_data = {
                    'repository_index': repository_index,
                    'repository_url': project_data['repository_url'],
                    'repository_hexsha': project_data['repository_hexsha'],
                    'project_pathname': project_pathname,
                    'classpath_pathnames': classpath_pathnames,
                    'focal_classpath': focal_classpath,
                    'focal_method_sample': focal_method_sample,
                }
                yield focal_method_data

    def _create_project_data_generator(
        self: Self,
        repository_samples: Iterator[dict[str, Any]],
    ) -> Generator[dict[str, Any], None, None]:
        for i, repository_sample in enumerate(repository_samples):
            repository_url = repository_sample['repository_url']
            logging.info(f'repository {i} url: {repository_url}')
            with tempfile.TemporaryDirectory() as temp_dir_pathname:
                logging.info(f'repository {i} dir: {temp_dir_pathname}')
                try:
                    repo = (
                        git.Repo.clone_from(repository_url, temp_dir_pathname))
                    project = (projects
                        .create_project(temp_dir_pathname, temp_dir_pathname))
                    subproject_pathnames = (
                        project.find_subproject_pathnames())
                except Exception as exception:
                    logging.warn(f'repository {i}: {exception}')
                    logging.debug(f'{traceback.format_exc()}')
                    continue
                for subproject_pathname in subproject_pathnames:
                    project_data = {
                        'repository_index': i,
                        'repository_url': repository_url,
                        'repository_hexsha': repo.head.commit.hexsha,
                        'root_pathname': temp_dir_pathname,
                        'project_pathname': subproject_pathname,
                    }
                    yield project_data

    def _add_coverage_data(
        self: Self,
        focal_method_sample: dict[str, Any],
        classpath_pathnames: list[str],
        focal_classpath: str,
        project_pathname: str,
    ) -> dict[str, Any]:
        focal_method: dict[str, Any] = focal_method_sample['focal_method']
        focal_method_line_start: int = focal_method['line_start']
        focal_method_line_end: int = focal_method['line_end']
        focal_method_body: str = focal_method['body']
        focal_method_lines: list[str] = focal_method_body.split('\n')
        focal_class: dict[str, Any] = focal_method['class']
        focal_package: str = focal_class['package']
        focal_class_identifier: str = focal_class['identifier']
        focal_class_name = f'{focal_package}.{focal_class_identifier}'
        test_methods: list[dict[str, Any]] = (
            focal_method_sample['test_methods'])
        with_coverage_test_methods = list()
        for test_method in test_methods:
            test_class: dict[str, Any] = test_method['class']
            test_package: str = test_class['package']
            test_class_identifier: str = test_class['identifier']
            test_class_name = f'{test_package}.{test_class_identifier}'
            test_method_name: str = test_method['identifier']
            request_data = coverages.CreateCoverageRequestData(
                classpathPathnames=classpath_pathnames,
                focalClasspath=focal_classpath,
                focalClassName=focal_class_name,
                testClassName=test_class_name,
                testMethodName=test_method_name,
            )
            try:
                with utilities.WorkingDirectory(project_pathname):
                    coverage = self._code_cov.create_coverage(request_data)
            except Exception as exception:
                logging.warn(f'{exception}')
                logging.debug(f'{traceback.format_exc()}')
                continue
            covered_line_indices: list[int] = list()
            covered_lines: list[str] = list()
            for covered_line_number in coverage['coveredLineNumbers']:
                covered_line_index = covered_line_number - 1
                if (covered_line_index < focal_method_line_start
                    or covered_line_index > focal_method_line_end):
                    continue
                i = covered_line_index - focal_method_line_start
                covered_line_indices.append(covered_line_index)
                covered_lines.append(focal_method_lines[i])
            with_coverage_test_method = copy.deepcopy(test_method)
            with_coverage_test_method['focal_covered_line_indices'] = (
                covered_line_indices)
            with_coverage_test_method['focal_covered_lines'] = covered_lines
            with_coverage_test_methods.append(with_coverage_test_method)
        with_coverage_focal_method_sample = (
            copy.deepcopy(focal_method_sample))
        with_coverage_focal_method_sample['test_methods'] = (
            with_coverage_test_methods)
        return with_coverage_focal_method_sample

    def _generate_samples(
        self: Self,
        repository_url: str,
        repository_hexsha: str,
        focal_method_sample: dict[str, Any],
    ) -> Generator[dict[str, str], None, None]:
        focal_method: dict[str, Any] = focal_method_sample['focal_method']
        focal_method_identifier: str = focal_method['identifier']
        focal_method_line_start: int = focal_method['line_start']
        focal_method_col_start: int = focal_method['col_start']
        focal_method_line_end: int = focal_method['line_end']
        focal_method_col_end: int = focal_method['col_end']
        focal_method_body: str = focal_method['body']
        focal_method_lines: list[str] = focal_method_body.split('\n')
        focal_class: dict[str, Any] = focal_method['class']
        focal_package: str = focal_class['package']
        focal_class_identifier: str = focal_class['identifier']
        focal_file: str = focal_class['file']
        test_methods: list[dict[str, Any]] = focal_method_sample['test_methods']
        for i, test_method_i in enumerate(test_methods):
            test_method_i_identifier: str = test_method_i['identifier']
            test_method_i_line_start: int = test_method_i['line_start']
            test_method_i_col_start: int = test_method_i['col_start']
            test_method_i_line_end: int = test_method_i['line_end']
            test_method_i_col_end: int = test_method_i['col_end']
            test_method_i_body: str = test_method_i['body']
            test_class: dict[str, Any] = test_method_i['class']
            test_package: str = test_class['package']
            test_class_identifier: str = test_class['identifier']
            test_file: str = test_class['file']
            i_covered_line_indices: list[int] = (
                test_method_i['focal_covered_line_indices'])
            i_covered_lines: list[str] = test_method_i['focal_covered_lines']
            for j, test_method_j in enumerate(test_methods):
                if i == j:
                    continue
                j_covered_line_indices: list[int] = (
                    test_method_j['focal_covered_line_indices'])
                i_uncovered_line_indices = sorted(
                    set(j_covered_line_indices) - set(i_covered_line_indices))
                if len(i_uncovered_line_indices) < 1:
                    continue
                j_covered_lines: list[str] = (
                    test_method_j['focal_covered_lines'])
                i_uncovered_lines: list[str] = list()
                for i_uncovered_line_index in i_uncovered_line_indices:
                    i = i_uncovered_line_index - focal_method_line_start
                    i_uncovered_lines.append(focal_method_lines[i])
                test_method_j_identifier: str = test_method_j['identifier']
                test_method_j_line_start: int = test_method_j['line_start']
                test_method_j_col_start: int = test_method_j['col_start']
                test_method_j_line_end: int = test_method_j['line_end']
                test_method_j_col_end: int = test_method_j['col_end']
                test_method_j_body: str = test_method_j['body']
                sample_repository = dict(
                    repository_url=repository_url,
                    repository_hexsha=repository_hexsha,
                )
                sample_focal_class = dict(
                    package=focal_package,
                    identifier=focal_class_identifier,
                )
                sample_focal_method = dict(
                    identifier=focal_method_identifier,
                    line_start=focal_method_line_start,
                    col_start=focal_method_col_start,
                    line_end=focal_method_line_end,
                    col_end=focal_method_col_end,
                    body=focal_method_body,
                )
                sample_test_class = dict(
                    package=test_package,
                    identifier=test_class_identifier,
                )
                sample_test_input_method = dict(
                    identifier=test_method_i_identifier,
                    line_start=test_method_i_line_start,
                    col_start=test_method_i_col_start,
                    line_end=test_method_i_line_end,
                    col_end=test_method_i_col_end,
                    body=test_method_i_body,
                    covered_line_indices=i_covered_line_indices,
                    covered_lines=i_covered_lines,
                )
                sample_test_target_method = dict(
                    identifier=test_method_j_identifier,
                    line_start=test_method_j_line_start,
                    col_start=test_method_j_col_start,
                    line_end=test_method_j_line_end,
                    col_end=test_method_j_col_end,
                    body=test_method_j_body,
                    covered_line_indices=j_covered_line_indices,
                    covered_lines=j_covered_lines,
                )
                sample = dict(
                    repository=sample_repository,
                    focal_file=focal_file,
                    focal_class=sample_focal_class,
                    focal_method=sample_focal_method,
                    focal_line_indices=i_uncovered_line_indices,
                    focal_lines=i_uncovered_lines,
                    test_file=test_file,
                    test_class=sample_test_class,
                    test_input_method=sample_test_input_method,
                    test_target_method=sample_test_target_method,
                )
                yield sample


class UniqueCoverageSamplesProcessor(Processor[dict[str, Any], dict[str, Any]]):
    def __init__(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, Any]],
    ) -> None:
        self._loader = loader
        self._saver = saver
        self._unique_method_triplets = set()

    def process(self: Self) -> None:
        samples = self._loader.load()
        def create_generator():
            for i, sample in enumerate(samples):
                logging.info(f'sample {i}')
                if not self._is_unique(sample):
                    continue
                yield sample
        iterator = utilities.GeneratorFunctionIterator(create_generator)
        self._saver.save(iterator)

    def _is_unique(self: Self, sample: dict[str, Any]) -> bool:
        method_triplet = (
            sample['focal_method']['body'],
            sample['test_input_method']['body'],
            sample['test_target_method']['body'],
        )
        if method_triplet in self._unique_method_triplets:
            return False
        self._unique_method_triplets.add(method_triplet)
        return True
