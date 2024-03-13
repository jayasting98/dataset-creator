import os
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


class CodeCovApi:
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
    ) -> requests.Response:
        url = os.path.join(self._base_url, 'coverages')
        response = (
            self._session.post(url, json=request_data, timeout=self._timeout))
        return response
