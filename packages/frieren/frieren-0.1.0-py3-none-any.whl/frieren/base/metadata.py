from dataclasses import dataclass, field
from typing import TypeVar


@dataclass
class Metadata:
    stem: str
    suffix: str
    prefix: str = field(default="")

    @property
    def filename(self) -> str:
        return self.prefix + self.stem + self.suffix


MetadataT = TypeVar("MetadataT", bound=Metadata)
