import abc
from typing import Any
from typing import Generic
from typing import Iterator
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
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
        limit: int | None = None,
    ) -> None:
        self._config = dict(streaming=True, **config)
        self._skip = skip
        self._limit = limit

    def load(self: Self) -> Iterator[dict[str, Any]]:
        dataset = datasets.load_dataset(**self._config)
        def create_generator():
            ds_iterator = iter(dataset)
            if self._skip is not None:
                for _ in range(self._skip):
                    next(ds_iterator, None)
            i = 0
            for sample in ds_iterator:
                yield sample
                if self._limit is None:
                    continue
                i += 1
                if i >= self._limit:
                    break
        iterator = utilities.GeneratorFunctionIterator(create_generator)
        return iterator


class HuggingFaceMultiLoader(Loader[dict[str, Any]]):
    def __init__(
        self: Self,
        configs: list[dict[str, Any]],
        skip: int | None = None,
        limit: int | None = None,
    ) -> None:
        self._configs = [dict(streaming=True, **config) for config in configs]
        self._skip = skip
        self._limit = limit

    def load(self: Self) -> Iterator[dict[str, Any]]:
        dsets = [datasets.load_dataset(**config) for config in self._configs]
        dataset = datasets.concatenate_datasets(dsets)
        def create_generator():
            ds_iterator = iter(dataset)
            if self._skip is not None:
                for _ in range(self._skip):
                    next(ds_iterator, None)
            i = 0
            for sample in ds_iterator:
                yield sample
                if self._limit is None:
                    continue
                i += 1
                if i >= self._limit:
                    break
        iterator = utilities.GeneratorFunctionIterator(create_generator)
        return iterator
