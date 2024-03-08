from typing import TypedDict


class CreateCoverageRequestData(TypedDict):
    jarPathnames: list[str]
    focalClasspath: str
    testClasspath: str
    focalClassName: str
    testClassName: str
    testMethodName: str
