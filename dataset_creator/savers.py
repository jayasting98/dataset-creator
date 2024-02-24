import abc
from typing import Any
from typing import Generic
from typing import Iterable
from typing import Self
from typing import TypeVar


_T = TypeVar('_T')


class Saver(abc.ABC, Generic[_T]):
    @abc.abstractmethod
    def __init__(self: Self, config: dict[str, Any]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self: Self, samples: Iterable[_T]) -> None:
        raise NotImplementedError()


class TextSaver(Saver[str]):
    def __init__(self: Self, config: dict[str, Any]) -> None:
        self._file_pathname = config['file_pathname']

    def save(self: Self, samples: Iterable[str]) -> None:
        lines = [f'{sample.strip()}\n' for sample in samples]
        with open(self._file_pathname, mode='a') as file:
            file.writelines(lines)
