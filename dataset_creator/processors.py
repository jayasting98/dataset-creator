import abc
from typing import Any
from typing import Generic
from typing import Self
from typing import TypeVar

from dataset_creator import loaders
from dataset_creator import savers
from dataset_creator import utilities


_T = TypeVar('_T')
_U = TypeVar('_U')


class Processor(abc.ABC, Generic[_T, _U]):
    @abc.abstractmethod
    def process(self: Self) -> None:
        raise NotImplementedError()


class TheStackRepositoryProcessor(Processor[dict[str, Any], dict[str, str]]):
    def __init__(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, str]],
    ) -> None:
        self._loader = loader
        self._saver = saver
        self._unique_repository_names = set()

    def process(self: Self) -> None:
        samples = self._loader.load()
        def create_generator():
            for sample in samples:
                repository_name = sample['max_stars_repo_name']
                if not self._is_unique(repository_name):
                    continue
                yield {'repository_name': repository_name}
        iterator = utilities.GeneratorFunctionIterator(create_generator)
        self._saver.save(iterator)

    def _is_unique(self: Self, repository_name: str) -> bool:
        if repository_name in self._unique_repository_names:
            return False
        self._unique_repository_names.add(repository_name)
        return True
