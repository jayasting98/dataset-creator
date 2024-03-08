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


class MavenRepository(Repository):
    def __init__(self: Self, root_dir_pathname: str) -> None:
        self._root_dir_pathname = root_dir_pathname

    def compile(self: Self) -> None:
        return super().compile()

    def get_jar_pathnames(self: Self) -> list[str]:
        return super().get_jar_pathnames()

    def get_focal_classpath(self: Self) -> str:
        return super().get_focal_classpath()

    def get_test_classpath(self: Self) -> str:
        return super().get_test_classpath()

    def get_focal_class_name(self: Self) -> str:
        return super().get_focal_class_name()

    def get_test_class_name(self: Self) -> str:
        return super().get_test_class_name()

    def get_test_method_name(self: Self) -> str:
        return super().get_test_method_name()
