import unittest
from unittest import mock

from dataset_creator import coverages


class CodeCovApiTest(unittest.TestCase):
    def test_create_coverage__typical_case__creates_coverage(self):
        session = mock.MagicMock()
        expected_response = mock.MagicMock()
        def do_side_effect(path, json=None):
            if path != 'http://localhost:8080/coverages':
                self.fail(msg=path)
            if json is None:
                self.fail()
            if not isinstance(json, dict):
                self.fail()
            if 'jarPathnames' not in json or json['jarPathnames'] is None:
                self.fail()
            if 'focalClasspath' not in json or json['focalClasspath'] is None:
                self.fail()
            if 'testClasspath' not in json or json['testClasspath'] is None:
                self.fail()
            if 'focalClassName' not in json or json['focalClassName'] is None:
                self.fail()
            if 'testClassName' not in json or json['testClassName'] is None:
                self.fail()
            if 'testMethodName' not in json or json['testMethodName'] is None:
                self.fail()
            return expected_response
        session.post.side_effect = do_side_effect
        base_url = 'http://localhost:8080'
        code_cov_api = coverages.CodeCovApi(session, base_url)
        jar_pathnames = [
            '~/.m2/repository/junit/junit/4.11/junit-4.11.jar',
            '~/.m2/repository/org/mockito/mockito-core/3.12.4/'
                + 'mockito-core-3.12.4.jar',
            '~/.m2/repository/org/hamcrest/hamcrest-core/1.3/'
                + 'hamcrest-core-1.3.jar',
            '~/.m2/repository/net/bytebuddy/byte-buddy/1.11.13/'
                + 'byte-buddy-1.11.13.jar',
            '~/.m2/repository/net/bytebuddy/byte-buddy-agent/1.11.13/'
                + 'byte-buddy-agent-1.11.13.jar',
            '~/.m2/repository/org/objenesis/objenesis/3.2/objenesis-3.2.jar',
        ]
        focal_classpath = ('integration_tests/resources/repositories/'
            + 'guess-the-number/target/classes/')
        test_classpath = ('integration_tests/resources/repositories/'
            + 'guess-the-number/target/test-classes/')
        focal_class_name = 'com.example.guessthenumber.ui.CommandLineUi'
        test_class_name = 'com.example.guessthenumber.ui.CommandLineUiTest'
        test_method_name = 'testRun_ioExceptionThrown_exitsGracefully'
        request_data = coverages.CreateCoverageRequestData(
            jarPathnames=jar_pathnames, focalClasspath=focal_classpath,
            testClasspath=test_classpath, focalClassName=focal_class_name,
            testClassName=test_class_name, testMethodName=test_method_name)
        actual_response = code_cov_api.create_coverage(request_data)
        self.assertIs(expected_response, actual_response)
