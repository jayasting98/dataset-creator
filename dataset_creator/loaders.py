import abc
from typing import Any
from typing import Generic
from typing import Iterator
from typing import Self
from typing import TypeVar

import datasets


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
        iterator = self._create_iterator(dataset)
        return iterator

    def _create_iterator(
        self: Self,
        dataset: datasets.Dataset | datasets.IterableDataset,
    ) -> Iterator[dict[str, Any]]:
        for sample in dataset:
            yield sample
