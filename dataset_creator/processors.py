import abc
from typing import Any
from typing import Generic
from typing import Self
from typing import TypeVar

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
