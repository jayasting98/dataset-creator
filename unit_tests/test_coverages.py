import os
import pathlib
from typing import Any
from typing import Protocol
from typing import Self
import unittest
from unittest import mock

from dataset_creator import coverages


class _SessionPost(Protocol):
    def __call__(
        self: Self,
        url: str,
        json: Any | None = None,
        timeout: int | None = None,
    ) -> mock.Mock:
        pass


class CodeCovApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self._base_url = 'http://localhost:8080'
        repo_dir_pathname = os.path.join(os.getcwd(), 'integration_tests',
            'resources', 'repositories', 'maven', 'guess-the-number')
        focal_classpath = (
            os.path.join(repo_dir_pathname, 'target', 'classes', ''))
        test_classpath = (
            os.path.join(repo_dir_pathname, 'target', 'test-classes', ''))
        home_dir_pathname = str(pathlib.Path.home())
        maven_dir_pathname = (
            os.path.join(home_dir_pathname, '.m2', 'repository'))
        classpath_pathnames = [
            focal_classpath,
            test_classpath,
            os.path.join(maven_dir_pathname, 'junit', 'junit', '4.11',
                'junit-4.11.jar'),
            os.path.join(maven_dir_pathname, 'org', 'mockito', 'mockito-core',
                '3.12.4', 'mockito-core-3.12.4.jar'),
            os.path.join(maven_dir_pathname, 'org', 'hamcrest', 'hamcrest-core',
                '1.3', 'hamcrest-core-1.3.jar'),
            os.path.join(maven_dir_pathname, 'net', 'bytebuddy', 'byte-buddy',
                '1.11.13', 'byte-buddy-1.11.13.jar'),
            os.path.join(maven_dir_pathname, 'net', 'bytebuddy',
                'byte-buddy-agent', '1.11.13', 'byte-buddy-agent-1.11.13.jar'),
            os.path.join(maven_dir_pathname, 'org', 'objenesis', 'objenesis',
                '3.2', 'objenesis-3.2.jar'),
        ]
        focal_class_name = 'com.example.guessthenumber.ui.CommandLineUi'
        test_class_name = (
            'com.example.guessthenumber.ui.CommandLineUiTest')
        test_method_name = 'testRun_ioExceptionThrown_exitsGracefully'
        self._request_data = coverages.CreateCoverageRequestData(
            classpathPathnames=classpath_pathnames,
            focalClasspath=focal_classpath,
            focalClassName=focal_class_name,
            testClassName=test_class_name,
            testMethodName=test_method_name,
        )

    def _create_side_effect(self, mock_response: mock.Mock) -> _SessionPost:
        def do_side_effect(
            url: str, json: Any | None = None, timeout: int | None = None):
            if url != 'http://localhost:8080/coverages':
                self.fail()
            if json is None:
                self.fail()
            if not isinstance(json, dict):
                self.fail()
            if ('classpathPathnames' not in json
                or json['classpathPathnames'] is None):
                self.fail()
            if 'focalClasspath' not in json or json['focalClasspath'] is None:
                self.fail()
            if 'focalClassName' not in json or json['focalClassName'] is None:
                self.fail()
            if 'testClassName' not in json or json['testClassName'] is None:
                self.fail()
            if 'testMethodName' not in json or json['testMethodName'] is None:
                self.fail()
            return mock_response
        return do_side_effect

    def test_create_coverage__typical_case__creates_coverage(self):
        mock_session = mock.MagicMock()
        mock_response = mock.MagicMock()
        expected_coverage = mock.MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = expected_coverage
        mock_session.post.side_effect = self._create_side_effect(mock_response)
        code_cov_api = coverages.CodeCovApi(mock_session, self._base_url)
        actual_coverage = code_cov_api.create_coverage(self._request_data)
        self.assertIs(expected_coverage, actual_coverage)

    def test_create_coverage__internal_server_error__raises_runtime_error(self):
        mock_session = mock.MagicMock()
        mock_response = mock.MagicMock()
        mock_response.status_code = 500
        mock_session.post.side_effect = self._create_side_effect(mock_response)
        code_cov_api = coverages.CodeCovApi(mock_session, self._base_url)
        with self.assertRaises(RuntimeError):
            code_cov_api.create_coverage(self._request_data)
