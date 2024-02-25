import abc
from typing import Any
from typing import Generic
from typing import Self
from typing import TypeVar

from dataset_creator import argument_parsers
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


@argument_parsers.parser_argument_choice('--creator', 'stack_local')
class TheStackRepositoryLocalDataFactory(
    CreatorFactory[dict[str, Any], dict[str, str]],
):
    def __init__(self: Self, config: dict[str, Any]) -> None:
        self._loader_config = config['loader']
        self._saver_config: dict[str, Any] = config['saver']

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        loader = loaders.HuggingFaceLoader(self._loader_config)
        return loader

    def create_saver(self: Self) -> savers.Saver[dict[str, str]]:
        file_pathname = self._saver_config['file_pathname']
        limit = self._saver_config.get('limit')
        saver = savers.LocalFileSaver(file_pathname, limit=limit)
        return saver

    def create_processor(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, str]],
    ) -> processors.Processor[dict[str, Any], dict[str, str]]:
        processor = processors.TheStackRepositoryProcessor(loader, saver)
        return processor


@argument_parsers.parser_argument_choice('--creator', 'stack_gcs')
class TheStackRepositoryHuggingFaceGoogleCloudStorageFactory(
    CreatorFactory[dict[str, Any], dict[str, str]],
):
    def __init__(self: Self, config: dict[str, Any]) -> None:
        self._loader_config = config['loader']
        self._saver_config: dict[str, Any] = config['saver']

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        loader = loaders.HuggingFaceLoader(self._loader_config)
        return loader

    def create_saver(self: Self) -> savers.Saver[dict[str, str]]:
        project_id = self._saver_config['project_id']
        bucket_name = self._saver_config['bucket_name']
        pathname = self._saver_config['pathname']
        limit = self._saver_config.get('limit')
        saver = savers.HuggingFaceGoogleCloudStorageSaver(
            project_id, bucket_name, pathname, limit=limit)
        return saver

    def create_processor(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, str]],
    ) -> processors.Processor[dict[str, Any], dict[str, str]]:
        processor = processors.TheStackRepositoryProcessor(loader, saver)
        return processor
