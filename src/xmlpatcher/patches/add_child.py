from typing import Any, Iterable

from lxml.etree import Element, _Element

from .patch import Patch


class AddChild(Patch):
    def __init__(self, xpath: str, child_name: str, child_value: str) -> None:
        """
        Adds a child element to the selected elements.
        :param xpath: An XPath pointer to the relevant XML element(s).
        :param child_name: The name of the new child element.
        :param child_value: The value of the new child element.
        """

        super().__init__(xpath)
        self.child_name = child_name
        self.child_value = child_value

    def _apply(self, objects: Iterable[Any]) -> None:
        for obj in objects:
            if not isinstance(obj, _Element):
                raise ValueError(f"Can only use the AddChild patch on an element. Got: {type(obj)}")
            obj.append(Element(self.child_name, text=self.child_value))
