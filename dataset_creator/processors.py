import abc
from typing import Any
from typing import Generic
from typing import Self
from typing import TypeVar

import datasets

from dataset_creator.loaders import Loader
from dataset_creator.savers import Saver


_T = TypeVar('_T')
_U = TypeVar('_U')


class Processor(abc.ABC, Generic[_T, _U]):
    @abc.abstractmethod
    def __init__(
        self: Self,
        loader: Loader[_T],
        saver: Saver[_U],
        config: dict[str, Any],
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def process(self: Self) -> None:
        raise NotImplementedError()


class TheStackRepositoryProcessor(Processor[dict[str, Any], str]):
    def __init__(
        self: Self,
        loader: Loader[_T],
        saver: Saver[_U],
        config: dict[str, Any],
    ) -> None:
        self._loader = loader
        self._saver = saver
        self._unique_repository_names = set()

    def process(self: Self) -> None:
        dataset: datasets.IterableDataset | datasets.Dataset
        dataset = self._loader.load()
        repository_ds = dataset.select_columns('max_stars_repo_name')
        deduplicated_ds = repository_ds.filter(self._is_unique)
        self._saver.save(deduplicated_ds)

    def _is_unique(self: Self, sample: dict[str, str]) -> bool:
        repository_name = sample['max_stars_repo_name']
        if repository_name in self._unique_repository_names:
            return False
        self._unique_repository_names.add(repository_name)
        return True
