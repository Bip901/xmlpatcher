from contextlib import contextmanager, nullcontext
from io import BytesIO
from os import remove
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import IO, Generator, Optional, Union

import lxml.etree

from .patches import Patch


class XMLDocument:
    def __init__(self, path: Union[Path, str], encoding: Optional[str] = None, remove_blank_text: bool = True) -> None:
        if isinstance(path, str):
            path = Path(path)
        self._path = path
        with path.open("rb") as f:
            parser = lxml.etree.XMLParser(encoding=encoding, remove_blank_text=remove_blank_text)
            self._tree: lxml.etree._ElementTree = lxml.etree.parse(f, parser)

    def patch(self, *patches: Patch) -> "XMLDocument":
        """
        Applies the given XML patches to this document.

        :returns: self
        """

        for patch in patches:
            patch.apply(self._tree)
        return self

    def save(self, target_file: Union[str, Path, IO[bytes], None] = None, pretty_print: bool = True) -> None:
        """
        Saves this object to disk.

        :param target_path: The path or file to save to, or None to save over the original file.
        """

        if target_file is None:
            target_file = self._path
        if hasattr(target_file, "write"):
            context = nullcontext()  # Don't close file if it's provided by caller
        else:
            context = target_file = open(target_file, "wb")
        with context:
            self._tree.write(
                target_file, xml_declaration=True, encoding="UTF-8", standalone=True, pretty_print=pretty_print
            )

    @contextmanager
    def save_to_temp_file(self, pretty_print: bool = True) -> Generator[str, None, None]:
        """
        Creates a new temporary .xml file and serializes this object to it.

        :returns: A context manager that yields the path of the temporary file and deletes it when closed.
        """

        with NamedTemporaryFile(suffix=".xml", delete=False) as tempfile:
            self.save(tempfile, pretty_print=pretty_print)
        yield tempfile.name
        remove(tempfile.name)

    def save_element(self, xpath: str, target_path: Union[str, Path], pretty_print: bool = True) -> bool:
        """
        Saves the first element matching the XPath to the target file.
        If no element matches, does nothing.

        :returns: Whether an element was found and saved.
        """

        result = self._tree.xpath(xpath)
        if isinstance(result, list):
            result = result[0] if len(result) else None
        if isinstance(result, lxml.etree._Element):
            with open(target_path, "wb") as f:
                lxml.etree.ElementTree(result).write(f, pretty_print=pretty_print)
            return True
        return False

    def load_element(self, xpath: str, from_path: Union[str, Path]) -> bool:
        """
        Replaces the first element in this document matching XPath with the contents of 'from_path'.
        If 'from_path' does not exist, does nothing.

        :returns: Whether the element was loaded.
        """

        if isinstance(from_path, str):
            from_path = Path(from_path)
        if not from_path.exists():
            return False
        other_document = XMLDocument(from_path)
        element = self._tree.xpath(xpath)
        if isinstance(element, list):
            element = element[0]
        element: lxml.etree._Element
        parent = element.getparent()
        if parent is None:
            self._tree = other_document._tree
        else:
            parent.replace(element, other_document._tree.getroot())
        return True

    def __str__(self) -> str:
        with BytesIO() as s:
            self._tree.write(s, xml_declaration=True, encoding="UTF-8", standalone=True, pretty_print=True)
            return s.getvalue().decode()
