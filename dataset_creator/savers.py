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
