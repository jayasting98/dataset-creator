import abc
from typing import Any
from typing import Generic
from typing import Iterator
from typing import Self
from typing import TypeVar

import datasets

from dataset_creator import utilities


_T = TypeVar('_T')


class Loader(abc.ABC, Generic[_T]):
    @abc.abstractmethod
    def load(self: Self) -> Iterator[_T]:
        raise NotImplementedError()


class HuggingFaceLoader(Loader[dict[str, Any]]):
    def __init__(self: Self, config: dict[str, Any]) -> None:
        self._config = dict(streaming=True, **config)

    def load(self: Self) -> Iterator[dict[str, Any]]:
        dataset = datasets.load_dataset(**self._config)
        def create_generator():
            for sample in dataset:
                yield sample
        iterator = utilities.GeneratorFunctionIterator(create_generator)
        return iterator
