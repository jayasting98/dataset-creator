import abc
from typing import Any
from typing import Generic
from typing import Self
from typing import TypeVar

from dataset_creator import loaders
from dataset_creator import processors
from dataset_creator import savers


_T = TypeVar('_T')
_U = TypeVar('_U')


class CreatorFactory(abc.ABC, Generic[_T, _U]):
    @abc.abstractmethod
    def __init__(self: Self, config: dict[str, Any]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_loader(self: Self) -> loaders.Loader[_T]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_saver(self: Self) -> savers.Saver[_U]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_processor(
        self: Self,
        loader: loaders.Loader[_T],
        saver: savers.Saver[_U],
    ) -> processors.Processor[_T, _U]:
        raise NotImplementedError()
