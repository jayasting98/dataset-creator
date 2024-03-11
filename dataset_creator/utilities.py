from collections.abc import Callable
from collections.abc import Generator
from collections.abc import Iterator
import os
import re
from types import TracebackType
from typing import Self
from typing import TypeVar


_T = TypeVar('_T')


class GeneratorFunctionIterator(Iterator[_T]):
    """An iterator wrapping around a generator (function).

    While generators are iterators, it is not possible to use pickle with
    generator objects in general. Using this allows us to continue to somewhat
    use generators as iterators. This works because unlike generator objects, it
    is possible to use pickle with generator functions.
    """
    def __init__(
        self: Self,
        generator_function: Callable[[], Generator[_T, None, None]],
    ) -> None:
        self._generator_function = generator_function

    def __iter__(self: Self) -> Iterator[_T]:
        return self

    def __next__(self: Self) -> _T:
        try:
            next_ = next(self._generator)
        except AttributeError:
            self._generator = self._generator_function()
            next_ = next(self._generator)
        return next_


class WorkingDirectory:
    """A context manager for executing code in a specified working directory."""
    def __init__(self: Self, working_dir_pathname: str) -> None:
        self._working_dir_pathname = working_dir_pathname

    def __enter__(self: Self) -> None:
        self._original_working_dir_pathname = os.getcwd()
        os.chdir(self._working_dir_pathname)

    def __exit__(
        self: Self,
        exception_type: type[BaseException],
        exception_value: BaseException,
        exception_traceback: TracebackType,
    ) -> bool:
        os.chdir(self._original_working_dir_pathname)
        return False


_CONSECUTIVE_UNDERSCORES_RE = re.compile(r'(?<=_)_')
_SNAKE_CASE_RE = re.compile(r'(?<=\w)_')


def space_out_snake_case(x: str) -> str:
    single_underscore_str = _CONSECUTIVE_UNDERSCORES_RE.sub(str(), x)
    spaced_out_str = _SNAKE_CASE_RE.sub(' ', single_underscore_str)
    return spaced_out_str


_STANDARD_CAMEL_CASE_RE = re.compile(r'([a-z\d])([A-Z])')
_ACRONYM_CAMEL_CASE_RE = re.compile(r'(\w)([A-Z][a-z]+)')


def space_out_camel_case(x: str) -> str:
    exclude_acronym_str = _STANDARD_CAMEL_CASE_RE.sub(r'\1 \2', x)
    spaced_out_str = _ACRONYM_CAMEL_CASE_RE.sub(r'\1 \2', exclude_acronym_str)
    return spaced_out_str
