from abc import ABC
from typing import TypeVar


class BaseRepository(ABC):
    pass


RepositoryT = TypeVar("RepositoryT", bound=BaseRepository)
