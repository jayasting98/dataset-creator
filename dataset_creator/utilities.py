from collections.abc import Callable
from collections.abc import Generator
from collections.abc import Iterator
import os
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
