from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeVar


from .repository import RepositoryT
from .metadata import MetadataT


@dataclass
class BaseLocator(Generic[RepositoryT, MetadataT]):
    repository: RepositoryT

    @property
    @abstractmethod
    def save_dir(self) -> Path:
        pass

    @abstractmethod
    def get_path(self, metadata: MetadataT) -> Path:
        pass


LocatorT = TypeVar("LocatorT", bound=BaseLocator)
