import abc
from typing import Iterable

from apitest.model_maps import APIMetadata, EndPoint


class APIImporter(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def metadata(self) -> APIMetadata:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def end_points(self) -> Iterable[EndPoint]:
        raise NotImplementedError()
