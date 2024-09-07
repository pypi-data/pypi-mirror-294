from abc import ABC, abstractmethod
from pathlib import Path
from typing import Type, ClassVar, Generic, TypeVar


from .metadata import MetadataT
from .locator import LocatorT
from .dtypes import FileT


class BaseOperator(ABC, Generic[LocatorT, MetadataT, FileT]):
    LocatorClass: ClassVar[Type[LocatorT]]

    def __init__(self, metadata: MetadataT):
        self.metadata = metadata

    def get_path(self, router: LocatorT) -> Path:
        if not isinstance(router, self.LocatorClass):
            raise TypeError(f"Expected instance of {self.LocatorClass.__name__}")
        path = router.get_path(self.metadata)
        return path

    @abstractmethod
    def save_file(self, obj: FileT, path: Path):
        pass

    def write(self, obj: FileT, config: LocatorT):
        path = self.get_path(config)
        path.parent.mkdir(exist_ok=True, parents=True)
        self.save_file(obj, path)

    @abstractmethod
    def load_file(self, path: Path) -> FileT:
        pass

    def read(self, config: LocatorT) -> FileT:
        path = self.get_path(config)
        return self.load_file(path)


OperatorT = TypeVar("OperatorT", bound=BaseOperator)
