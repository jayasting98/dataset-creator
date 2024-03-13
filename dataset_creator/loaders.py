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
    def __init__(
        self: Self,
        config: dict[str, Any],
        skip: int | None = None,
    ) -> None:
        self._config = dict(streaming=True, **config)
        self._skip = skip

    def load(self: Self) -> Iterator[dict[str, Any]]:
        dataset = datasets.load_dataset(**self._config)
        def create_generator():
            ds_iterator = iter(dataset)
            if self._skip is not None:
                for _ in range(self._skip):
                    next(ds_iterator, None)
            for sample in ds_iterator:
                yield sample
        iterator = utilities.GeneratorFunctionIterator(create_generator)
        return iterator
