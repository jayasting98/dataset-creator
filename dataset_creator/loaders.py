import abc
from typing import Any
from typing import Generic
from typing import Iterable
from typing import Self
from typing import TypeVar

import datasets


_T = TypeVar('_T')


class Loader(abc.ABC, Generic[_T]):
    @abc.abstractmethod
    def __init__(self: Self, config: dict[str, Any]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def load(self: Self) -> Iterable[_T]:
        raise NotImplementedError()


class HuggingFaceLoader(Loader[_T]):
    def __init__(self: Self, config: dict[str, Any]) -> None:
        self._config = dict(streaming=True, **config)

    def load(self: Self) -> Iterable[_T]:
        dataset = datasets.load_dataset(**self._config)
        return dataset
