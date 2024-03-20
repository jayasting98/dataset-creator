import abc
import json
import logging
import os
import subprocess
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
from typing import TypedDict

import requests


class CreateCoverageRequestData(TypedDict):
    classpathPathnames: list[str]
    focalClasspath: str
    focalClassName: str
    testClassName: str
    testMethodName: str


class Coverage(TypedDict):
    coveredLineNumbers: list[int]


class CodeCov(abc.ABC):
    @abc.abstractmethod
    def create_coverage(
        self: Self,
        request_data: CreateCoverageRequestData,
    ) -> Coverage:
        raise NotImplementedError()


class CodeCovApi(CodeCov):
    def __init__(
        self: Self,
        session: requests.Session,
        base_url: str,
        timeout: int | None = None,
    ) -> None:
        self._session = session
        self._base_url = base_url
        self._timeout = timeout

    def create_coverage(
        self: Self,
        request_data: CreateCoverageRequestData,
    ) -> Coverage:
        url = os.path.join(self._base_url, 'coverages')
        logging.debug('{url} POST ({fcn}, {tcn}, {tmn})'.format(url=url,
            fcn=request_data['focalClassName'],
            tcn=request_data['testClassName'],
            tmn=request_data['testMethodName']))
        response = (
            self._session.post(url, json=request_data, timeout=self._timeout))
        if not 200 <= response.status_code <= 299:
            raise RuntimeError(f'coverage not found: {request_data}')
        coverage: Coverage = response.json()
        return coverage


class CodeCovCli(CodeCov):
    def __init__(
        self: Self,
        script_file_pathname: str,
        timeout: int | None = None,
    ) -> None:
        self._script_file_pathname = script_file_pathname
        self._timeout = timeout

    def create_coverage(
        self: Self,
        request_data: CreateCoverageRequestData,
    ) -> Coverage:
        input_json_arg = json.dumps(request_data)
        args = [self._script_file_pathname, input_json_arg]
        completed_process = (subprocess
            .run(args, timeout=self._timeout, check=True, capture_output=True))
        output = completed_process.stdout
        coverage: Coverage = json.loads(output)
        return coverage
