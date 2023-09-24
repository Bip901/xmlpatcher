from typing import Any, Iterable

from lxml.etree import _Element, _ElementUnicodeResult

from .patch import Patch


class Remove(Patch):
    def __init__(self, xpath: str) -> None:
        """
        Removes the selected element or attribute.

        :param xpath: An XPath pointer to the relevant XML element or attribute.
        """

        super().__init__(xpath)

    def _apply(self, objects: Iterable[Any]) -> None:
        for obj in objects:
            if isinstance(obj, _Element):
                parent = obj.getparent()
                if parent is None:
                    raise ValueError("Can't remove the root element.")
                parent.remove(obj)
            elif isinstance(obj, _ElementUnicodeResult):
                attributes = obj.getparent().attrib
                attributes.pop(obj.attrname)
