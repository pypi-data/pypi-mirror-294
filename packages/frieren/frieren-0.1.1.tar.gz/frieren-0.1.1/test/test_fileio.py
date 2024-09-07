from dataclasses import dataclass
from pathlib import Path
from typing import Type

from frieren import BaseRepository, RepositoryT
from frieren import Metadata, MetadataT
from frieren import BaseLocator, LocatorT
from frieren import FileT
from frieren import BaseOperator, OperatorT


PYTEST_CACHE_DIR = Path(__file__).parent.parent / ".pytest_cache"


@dataclass
class User:
    usename: str


class Repository(BaseRepository):

    def __init__(self, user: User):
        self.user = user

    @property
    def data(self) -> Path:
        return PYTEST_CACHE_DIR / f"users/{self.user.usename}/data"


@dataclass
class Locator(BaseLocator[Repository, Metadata]):
    x: int = 1

    @property
    def save_dir(self):
        return self.repository.data / f"{self.x:0>1}"

    def get_path(self, metadata: Metadata):
        return self.save_dir / metadata.filename.replace(
            f"{metadata.suffix}", f"_{self.x:0>2}{metadata.suffix}"
        )


class SampleTxtOperator(BaseOperator[Locator, Metadata, str]):
    LocatorClass: Type[LocatorT] = Locator

    def save_file(self, obj: str, path: Path):
        with open(path, mode="w") as file:
            file.write(obj)

    def load_file(self, path) -> str:
        with open(path, mode="r") as file:
            return file.read()


def test_case_1():
    #
    # defined in module by developer
    #
    sample_txt_meta = Metadata("sample", ".txt", "")
    sample_txt_handler = SampleTxtOperator(sample_txt_meta)
    read_sample_txt = sample_txt_handler.read
    write_sample_txt = sample_txt_handler.write

    #
    # user scripts
    #
    repository = Repository(user=User("t-tanaka"))
    file_access_router = Locator(repository, x=5)

    input_text = "Sample Text"
    write_sample_txt(input_text, file_access_router)

    output_text = read_sample_txt(file_access_router)
    assert input_text == output_text
