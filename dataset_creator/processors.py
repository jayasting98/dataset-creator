import abc
import copy
import logging
import tempfile
import traceback
from typing import Any
from typing import Generic
from typing import Self
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
            for sample in samples:
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
        code_cov_api: coverages.CodeCovApi,
        parser: code_parsers.CodeParser,
    ) -> None:
        self._loader = loader
        self._saver = saver
        self._code_cov_api = code_cov_api
        self._parser = parser

    def process(self: Self) -> None:
        repository_samples = self._loader.load()
        def create_generator():
            for i, repository_sample in enumerate(repository_samples):
                repository_url = repository_sample['repository_url']
                logging.info(f'repository {i} URL: {repository_url}')
                with tempfile.TemporaryDirectory() as temp_dir_pathname:
                    logging.info(f'repository {i} Dir: {temp_dir_pathname}')
                    repo = (
                        git.Repo.clone_from(repository_url, temp_dir_pathname))
                    project = projects.create_project(temp_dir_pathname)
                    try:
                        subproject_pathnames = (
                            project.find_subproject_pathnames())
                    except Exception as exception:
                        logging.warn(f'{exception}')
                        logging.debug(f'{traceback.format_exc()}')
                        continue
                    for subproject_pathname in subproject_pathnames:
                        subproject = (
                            projects.create_project(subproject_pathname))
                        try:
                            samples = self._generate_project_samples(
                                repository_url, repo.head.commit.hexsha,
                                subproject)
                        except Exception as exception:
                            logging.warn(f'{exception}')
                            logging.debug(f'{traceback.format_exc()}')
                            continue
                        logging.debug(f'{samples}')
                        for samples in samples:
                            yield samples
        iterator = utilities.GeneratorFunctionIterator(create_generator)
        self._saver.save(iterator)

    def _generate_project_samples(
        self: Self,
        repository_url: str,
        repository_hexsha: str,
        project: projects.Project,
    ) -> list[dict[str, Any]]:
        logging.info('compiling')
        project.compile()
        logging.info('finding classpath')
        classpath_pathnames = project.find_classpath_pathnames()
        logging.info('finding focal classpath')
        focal_classpath = project.find_focal_classpath()
        logging.info('finding focal method samples')
        focal_method_samples = (find_map_test_cases
            .find_focal_method_samples(project.root_dir_pathname, self._parser))
        logging.info('adding coverage data')
        with_coverage_focal_method_samples = self._add_coverage_data(
            focal_method_samples, classpath_pathnames, focal_classpath)
        logging.debug(f'{with_coverage_focal_method_samples}')
        logging.info('generating samples')
        project_samples = list()
        for with_coverage_focal_method_sample in (
            with_coverage_focal_method_samples):
            samples = self._generate_samples(repository_url, repository_hexsha,
                with_coverage_focal_method_sample)
            project_samples.extend(samples)
        return project_samples

    def _add_coverage_data(
        self: Self,
        focal_method_samples: list[dict[str, Any]],
        classpath_pathnames: list[str],
        focal_classpath: str,
    ) -> list[dict[str, Any]]:
        with_coverage_focal_method_samples = list()
        for focal_method_sample in focal_method_samples:
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
                response = self._code_cov_api.create_coverage(request_data)
                if not 200 <= response.status_code <= 299:
                    continue
                coverage: coverages.Coverage = response.json()
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
            (with_coverage_focal_method_samples
                .append(with_coverage_focal_method_sample))
        return with_coverage_focal_method_samples

    def _generate_samples(
        self: Self,
        repository_url: str,
        repository_hexsha: str,
        focal_method_sample: dict[str, Any],
    ) -> list[dict[str, str]]:
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
        samples: list[dict[str, Any]] = list()
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
                samples.append(sample)
        return samples
