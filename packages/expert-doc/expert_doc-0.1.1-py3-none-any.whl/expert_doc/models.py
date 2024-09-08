import abc
from pathlib import Path
from typing import Iterable, NamedTuple


class Image(abc.ABC):
    @abc.abstractmethod
    def dump_to_file(self, name_no_extension: str) -> str:
        pass

    pass


class ParsedPage(NamedTuple):
    images: list[Image]
    text: str
    pass


class PagedDocParser(abc.ABC):
    def __init__(self, path: Path):
        self.path = path
        return

    @abc.abstractmethod
    def iter_pages(self) -> Iterable[ParsedPage]:
        pass

    pass
