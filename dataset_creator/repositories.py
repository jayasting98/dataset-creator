import abc
from typing import Self


class Repository(abc.ABC):
    @abc.abstractmethod
    def compile(self: Self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_jar_pathnames(self: Self) -> list[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_focal_classpath(self: Self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_test_classpath(self: Self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_focal_class_name(self: Self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_test_class_name(self: Self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_test_method_name(self: Self) -> str:
        raise NotImplementedError()
