from abc import ABC, abstractmethod
from typing import Any, Iterable

import lxml.etree


class Patch(ABC):
    def __init__(self, xpath: str) -> None:
        self.xpath = xpath

    def apply(self, document: lxml.etree._ElementTree) -> None:
        matches = document.xpath(self.xpath)
        if not isinstance(matches, list):
            matches = [matches]
        self._apply(matches)

    @abstractmethod
    def _apply(self, objects: Iterable[Any]) -> None:
        pass
