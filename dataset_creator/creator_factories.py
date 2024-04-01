import abc
import argparse
from typing import Any
from typing import Generic
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
from typing import TypeVar

import requests

from dataset_creator import argument_parsers
from dataset_creator import coverages
from dataset_creator import loaders
from dataset_creator import processors
from dataset_creator import savers
from dataset_creator.methods2test import code_parsers


_T = TypeVar('_T')
_U = TypeVar('_U')


class CreatorFactory(abc.ABC, Generic[_T, _U]):
    @abc.abstractmethod
    def __init__(
        self: Self,
        config: dict[str, Any],
        args: argparse.Namespace,
    ) -> None:
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
    def __init__(
        self: Self,
        config: dict[str, Any],
        args: argparse.Namespace,
    ) -> None:
        self._token = args.token
        self._loader_config: dict[str, Any] = config['loader']
        self._saver_config: dict[str, Any] = config['saver']

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        config = self._loader_config['config']
        try:
            config['storage_options']['token'] = self._token
        except KeyError:
            pass
        skip: int | None = self._loader_config.get('skip')
        limit: int | None = self._loader_config.get('limit')
        loader = loaders.HuggingFaceLoader(config, skip=skip, limit=limit)
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
    def __init__(
        self: Self,
        config: dict[str, Any],
        args: argparse.Namespace,
    ) -> None:
        self._token = args.token
        self._loader_config: dict[str, Any] = config['loader']
        self._saver_config: dict[str, Any] = config['saver']

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        config = self._loader_config['config']
        try:
            config['storage_options']['token'] = self._token
        except KeyError:
            pass
        skip: int | None = self._loader_config.get('skip')
        limit: int | None = self._loader_config.get('limit')
        loader = loaders.HuggingFaceLoader(config, skip=skip, limit=limit)
        return loader

    def create_saver(self: Self) -> savers.Saver[dict[str, str]]:
        project_id = self._saver_config['project_id']
        bucket_name = self._saver_config['bucket_name']
        pathname = self._saver_config['pathname']
        limit = self._saver_config.get('limit')
        saver = savers.HuggingFaceGoogleCloudStorageSaver(
            project_id, bucket_name, pathname, token=self._token, limit=limit)
        return saver

    def create_processor(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, str]],
    ) -> processors.Processor[dict[str, Any], dict[str, str]]:
        processor = processors.TheStackRepositoryProcessor(loader, saver)
        return processor


@argument_parsers.parser_argument_choice('--creator', 'local_stack_gcs')
class LocalTheStackRepositoryHuggingFaceGoogleCloudStorageFactory(
    CreatorFactory[dict[str, Any], dict[str, str]],
):
    def __init__(
        self: Self,
        config: dict[str, Any],
        args: argparse.Namespace,
    ) -> None:
        self._token = args.token
        self._loader_config: dict[str, Any] = config['loader']
        self._saver_config: dict[str, Any] = config['saver']

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        pathname: str = self._loader_config['pathname']
        loader = loaders.JsonlFileLoader(pathname)
        return loader

    def create_saver(self: Self) -> savers.Saver[dict[str, str]]:
        project_id = self._saver_config['project_id']
        bucket_name = self._saver_config['bucket_name']
        pathname = self._saver_config['pathname']
        limit = self._saver_config.get('limit')
        saver = savers.HuggingFaceGoogleCloudStorageSaver(
            project_id, bucket_name, pathname, token=self._token, limit=limit)
        return saver

    def create_processor(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, str]],
    ) -> processors.Processor[dict[str, Any], dict[str, str]]:
        processor = processors.TheStackRepositoryProcessor(loader, saver)
        return processor


@argument_parsers.parser_argument_choice('--creator', 'gcs_local')
class HuggingFaceGoogleCloudStorageToLocalDataFactory(
    CreatorFactory[dict[str, Any], dict[str, Any]],
):
    def __init__(
        self: Self,
        config: dict[str, Any],
        args: argparse.Namespace,
    ) -> None:
        self._token = args.token
        self._loader_config: dict[str, Any] = config['loader']
        self._saver_config: dict[str, Any] = config['saver']

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        config = self._loader_config['config']
        try:
            config['storage_options']['token'] = self._token
        except KeyError:
            pass
        skip: int | None = self._loader_config.get('skip')
        limit: int | None = self._loader_config.get('limit')
        loader = loaders.HuggingFaceLoader(config, skip=skip, limit=limit)
        return loader

    def create_saver(self: Self) -> savers.Saver[dict[str, str]]:
        file_pathname = self._saver_config['file_pathname']
        limit = self._saver_config.get('limit')
        saver = savers.LocalFileSaver(file_pathname, limit=limit)
        return saver

    def create_processor(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, Any]],
    ) -> processors.Processor[dict[str, Any], dict[str, Any]]:
        processor = processors.IdentityProcessor(loader, saver)
        return processor


@argument_parsers.parser_argument_choice('--creator', 'cov_api_local')
class CoverageApiLocalDataFactory(
    CreatorFactory[dict[str, Any], dict[str, Any]],
):
    def __init__(
        self: Self,
        config: dict[str, Any],
        args: argparse.Namespace,
    ) -> None:
        self._token = args.token
        self._loader_config: dict[str, Any] = config['loader']
        self._saver_config: dict[str, Any] = config['saver']
        self._base_url = config['base_url']
        self._grammar_file = config['grammar_file']
        self._language = config['language']
        self._timeout = config.get('timeout')

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        config = self._loader_config['config']
        try:
            config['storage_options']['token'] = self._token
        except KeyError:
            pass
        skip: int | None = self._loader_config.get('skip')
        limit: int | None = self._loader_config.get('limit')
        loader = loaders.HuggingFaceLoader(config, skip=skip, limit=limit)
        return loader

    def create_saver(self: Self) -> savers.Saver[dict[str, Any]]:
        file_pathname = self._saver_config['file_pathname']
        limit = self._saver_config.get('limit')
        saver = savers.LocalFileSaver(file_pathname, limit=limit)
        return saver

    def create_processor(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, Any]],
    ) -> processors.Processor[dict[str, Any], dict[str, Any]]:
        session = requests.Session()
        code_cov = (coverages
            .CodeCovApi(session, self._base_url, timeout=self._timeout))
        parser_type = code_parsers.CodeParser
        parser_args = (self._grammar_file, self._language)
        processor = processors.CoverageSamplesProcessor(loader, saver, code_cov,
            parser_type, parser_args)
        return processor


@argument_parsers.parser_argument_choice('--creator', 'cov_api_gcs')
class CoverageApiHuggingFaceGoogleCloudStorageFactory(
    CreatorFactory[dict[str, Any], dict[str, Any]],
):
    def __init__(
        self: Self,
        config: dict[str, Any],
        args: argparse.Namespace,
    ) -> None:
        self._token = args.token
        self._loader_config: dict[str, Any] = config['loader']
        self._saver_config: dict[str, Any] = config['saver']
        self._base_url = config['base_url']
        self._grammar_file = config['grammar_file']
        self._language = config['language']
        self._timeout = config.get('timeout')

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        config = self._loader_config['config']
        try:
            config['storage_options']['token'] = self._token
        except KeyError:
            pass
        skip: int | None = self._loader_config.get('skip')
        limit: int | None = self._loader_config.get('limit')
        loader = loaders.HuggingFaceLoader(config, skip=skip, limit=limit)
        return loader

    def create_saver(self: Self) -> savers.Saver[dict[str, Any]]:
        project_id = self._saver_config['project_id']
        bucket_name = self._saver_config['bucket_name']
        pathname = self._saver_config['pathname']
        limit = self._saver_config.get('limit')
        saver = savers.HuggingFaceGoogleCloudStorageSaver(
            project_id, bucket_name, pathname, token=self._token, limit=limit)
        return saver

    def create_processor(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, Any]],
    ) -> processors.Processor[dict[str, Any], dict[str, Any]]:
        session = requests.Session()
        code_cov = (coverages
            .CodeCovApi(session, self._base_url, timeout=self._timeout))
        parser_type = code_parsers.CodeParser
        parser_args = (self._grammar_file, self._language)
        processor = processors.CoverageSamplesProcessor(loader, saver, code_cov,
            parser_type, parser_args)
        return processor


@argument_parsers.parser_argument_choice('--creator', 'cov_cli_local')
class CoverageCliLocalDataFactory(
    CreatorFactory[dict[str, Any], dict[str, Any]],
):
    def __init__(
        self: Self,
        config: dict[str, Any],
        args: argparse.Namespace,
    ) -> None:
        self._token = args.token
        self._loader_config: dict[str, Any] = config['loader']
        self._saver_config: dict[str, Any] = config['saver']
        self._script_file_pathname = config['script_file_pathname']
        self._grammar_file = config['grammar_file']
        self._language = config['language']
        self._timeout = config.get('timeout')

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        config = self._loader_config['config']
        try:
            config['storage_options']['token'] = self._token
        except KeyError:
            pass
        skip: int | None = self._loader_config.get('skip')
        limit: int | None = self._loader_config.get('limit')
        loader = loaders.HuggingFaceLoader(config, skip=skip, limit=limit)
        return loader

    def create_saver(self: Self) -> savers.Saver[dict[str, Any]]:
        file_pathname = self._saver_config['file_pathname']
        limit = self._saver_config.get('limit')
        saver = savers.LocalFileSaver(file_pathname, limit=limit)
        return saver

    def create_processor(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, Any]],
    ) -> processors.Processor[dict[str, Any], dict[str, Any]]:
        code_cov = (coverages
            .CodeCovCli(self._script_file_pathname, timeout=self._timeout))
        parser_type = code_parsers.CodeParser
        parser_args = (self._grammar_file, self._language)
        processor = processors.CoverageSamplesProcessor(loader, saver, code_cov,
            parser_type, parser_args)
        return processor


@argument_parsers.parser_argument_choice('--creator', 'cov_cli_gcs')
class CoverageCliHuggingFaceGoogleCloudStorageFactory(
    CreatorFactory[dict[str, Any], dict[str, Any]],
):
    def __init__(
        self: Self,
        config: dict[str, Any],
        args: argparse.Namespace,
    ) -> None:
        self._token = args.token
        self._loader_config: dict[str, Any] = config['loader']
        self._saver_config: dict[str, Any] = config['saver']
        self._script_file_pathname = config['script_file_pathname']
        self._grammar_file = config['grammar_file']
        self._language = config['language']
        self._timeout = config.get('timeout')

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        config = self._loader_config['config']
        try:
            config['storage_options']['token'] = self._token
        except KeyError:
            pass
        skip: int | None = self._loader_config.get('skip')
        limit: int | None = self._loader_config.get('limit')
        loader = loaders.HuggingFaceLoader(config, skip=skip, limit=limit)
        return loader

    def create_saver(self: Self) -> savers.Saver[dict[str, Any]]:
        project_id = self._saver_config['project_id']
        bucket_name = self._saver_config['bucket_name']
        pathname = self._saver_config['pathname']
        limit = self._saver_config.get('limit')
        saver = savers.HuggingFaceGoogleCloudStorageSaver(
            project_id, bucket_name, pathname, token=self._token, limit=limit)
        return saver

    def create_processor(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, Any]],
    ) -> processors.Processor[dict[str, Any], dict[str, Any]]:
        code_cov = (coverages
            .CodeCovCli(self._script_file_pathname, timeout=self._timeout))
        parser_type = code_parsers.CodeParser
        parser_args = (self._grammar_file, self._language)
        processor = processors.CoverageSamplesProcessor(loader, saver, code_cov,
            parser_type, parser_args)
        return processor


@argument_parsers.parser_argument_choice('--creator', 'cov_cat_local')
class CoverageConcatenatedHuggingFaceGoogleCloudStorageFactory(
    CreatorFactory[dict[str, Any], dict[str, Any]],
):
    def __init__(
        self: Self,
        config: dict[str, Any],
        args: argparse.Namespace,
    ) -> None:
        self._token = args.token
        self._loader_config: dict[str, Any] = config['loader']
        self._saver_config: dict[str, Any] = config['saver']

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        configs = self._loader_config['configs']
        for config in configs:
            try:
                config['storage_options']['token'] = self._token
            except KeyError:
                continue
        skip: int | None = self._loader_config.get('skip')
        limit: int | None = self._loader_config.get('limit')
        loader = loaders.HuggingFaceMultiLoader(configs, skip=skip, limit=limit)
        return loader

    def create_saver(self: Self) -> savers.Saver[dict[str, Any]]:
        file_pathname = self._saver_config['file_pathname']
        limit = self._saver_config.get('limit')
        saver = savers.LocalFileSaver(file_pathname, limit=limit)
        return saver

    def create_processor(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, Any]],
    ) -> processors.Processor[dict[str, Any], dict[str, Any]]:
        processor = processors.UniqueCoverageSamplesProcessor(loader, saver)
        return processor


@argument_parsers.parser_argument_choice('--creator', 'cov_cat_gcs')
class CoverageConcatenatedHuggingFaceGoogleCloudStorageFactory(
    CreatorFactory[dict[str, Any], dict[str, Any]],
):
    def __init__(
        self: Self,
        config: dict[str, Any],
        args: argparse.Namespace,
    ) -> None:
        self._token = args.token
        self._loader_config: dict[str, Any] = config['loader']
        self._saver_config: dict[str, Any] = config['saver']

    def create_loader(self: Self) -> loaders.Loader[dict[str, Any]]:
        configs = self._loader_config['configs']
        for config in configs:
            try:
                config['storage_options']['token'] = self._token
            except KeyError:
                continue
        skip: int | None = self._loader_config.get('skip')
        limit: int | None = self._loader_config.get('limit')
        loader = loaders.HuggingFaceMultiLoader(configs, skip=skip, limit=limit)
        return loader

    def create_saver(self: Self) -> savers.Saver[dict[str, Any]]:
        project_id = self._saver_config['project_id']
        bucket_name = self._saver_config['bucket_name']
        pathname = self._saver_config['pathname']
        limit = self._saver_config.get('limit')
        saver = savers.HuggingFaceGoogleCloudStorageSaver(
            project_id, bucket_name, pathname, token=self._token, limit=limit)
        return saver

    def create_processor(
        self: Self,
        loader: loaders.Loader[dict[str, Any]],
        saver: savers.Saver[dict[str, Any]],
    ) -> processors.Processor[dict[str, Any], dict[str, Any]]:
        processor = processors.UniqueCoverageSamplesProcessor(loader, saver)
        return processor
