import abc
import os
import pathlib
from typing import Any
from typing import Generic
from typing import Iterator
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self
from typing import TypeVar

import datasets
import gcsfs


_T = TypeVar('_T')


class Saver(abc.ABC, Generic[_T]):
    @abc.abstractmethod
    def save(self: Self, samples: Iterator[_T]) -> None:
        raise NotImplementedError()


class LocalFileSaver(Saver[Any]):
    def __init__(
        self: Self,
        file_pathname: str,
        limit: int | None = None,
    ) -> None:
        self._file_pathname = file_pathname
        self._limit = limit

    def save(self: Self, samples: Iterator[Any]) -> None:
        file_parent_dir_path = pathlib.Path(self._file_pathname).parent
        file_parent_dir_path.mkdir(parents=True, exist_ok=True)
        i = 0
        with open(self._file_pathname, mode='a') as file:
            for sample in samples:
                sample_str = str(sample).strip()
                line = f'{sample_str}\n'
                file.write(line)
                if self._limit is None:
                    continue
                i += 1
                if i >= self._limit:
                    break


class HuggingFaceGoogleCloudStorageSaver(Saver[dict[str, str]]):
    def __init__(
        self: Self,
        project_id: str,
        bucket_name: str,
        pathname: str,
        token: dict[str, str] | str | None = None,
        limit: int | None = None,
    ) -> None:
        self._storage_options = {'project': project_id, 'token': token}
        self._file_system = gcsfs.GCSFileSystem(**self._storage_options)
        self._bucket_name = bucket_name
        self._pathname = pathname
        self._limit = limit

    def save(self: Self, samples: Iterator[dict[str, str]]) -> None:
        def generator():
            i = 0
            for sample in samples:
                yield sample
                if self._limit is None:
                    continue
                i += 1
                if i >= self._limit:
                    break
        dataset = datasets.Dataset.from_generator(generator)
        dataset_path = os.path.join(f'gs://{self._bucket_name}', self._pathname)
        (dataset
            .save_to_disk(dataset_path, storage_options=self._storage_options))
