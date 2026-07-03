from pathlib import Path

from .patches import Patch
from .xml_document import XMLDocument


class Transformation:
    def __init__(self, original: str | Path, copy: str | Path, *patches: Patch) -> None:
        self.original = original
        self.copy = copy
        self.patches = patches

    def apply(self) -> None:
        document = XMLDocument(self.original)
        document.patch(*self.patches)
        document.save(self.copy)
