from typing import Any, Iterable, Optional

from lxml.etree import _Element, _ElementUnicodeResult

from .patch import Patch


class SetValue(Patch):
    def __init__(self, xpath: str, new_value: Optional[str]) -> None:
        """
        Sets the text of an element, or sets the value of an attribute, or removes an attribute.

        :param xpath: An XPath pointer to the relevant XML element or attribute.
        :param new_value: The value to set the attribute/element to, or null to remove the attribute.
        """

        super().__init__(xpath)
        self.new_value = new_value

    def _apply(self, objects: Iterable[Any]) -> None:
        for obj in objects:
            if isinstance(obj, _Element):
                obj.text = self.new_value
            elif isinstance(obj, _ElementUnicodeResult):
                attributes = obj.getparent().attrib
                if self.new_value is None:
                    attributes.pop(obj.attrname)
                else:
                    attributes[obj.attrname] = self.new_value
