import abc
from typing import Any
from typing import Generic
from typing import Self
from typing import TypeVar

from dataset_creator.loaders import Loader
from dataset_creator.processors import Processor
from dataset_creator.savers import Saver


_T = TypeVar('_T')
_U = TypeVar('_U')


class CreatorFactory(abc.ABC, Generic[_T, _U]):
    @abc.abstractmethod
    def __init__(self: Self, config: dict[str, Any]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_loader(self: Self) -> Loader[_T]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_saver(self: Self) -> Saver[_U]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_processor(
        self: Self,
        loader: Loader[_T],
        saver: Saver[_U],
    ) -> Processor[_T, _U]:
        raise NotImplementedError()
