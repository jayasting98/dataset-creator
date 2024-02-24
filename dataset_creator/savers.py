import abc
from typing import Any
from typing import Generic
from typing import Iterator
from typing import Self
from typing import TypeVar


_T = TypeVar('_T')


class Saver(abc.ABC, Generic[_T]):
    @abc.abstractmethod
    def __init__(self: Self, config: dict[str, Any]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self: Self, samples: Iterator[_T]) -> None:
        raise NotImplementedError()


class LocalFileSaver(Saver[Any]):
    def __init__(self: Self, config: dict[str, Any]) -> None:
        self._file_pathname = config['file_pathname']

    def save(self: Self, samples: Iterator[Any]) -> None:
        with open(self._file_pathname, mode='a') as file:
            for sample in samples:
                sample_str = str(sample).strip()
                line = f'{sample_str}\n'
                file.write(line)
