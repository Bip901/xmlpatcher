from pathlib import Path
from typing import Union

from .patches import Patch
from .xml_document import XMLDocument


class Transformation:
    def __init__(self, original: Union[str, Path], copy: Union[str, Path], *patches: Patch) -> None:
        self.original = original
        self.copy = copy
        self.patches = patches

    def apply(self) -> None:
        document = XMLDocument(self.original)
        document.patch(*self.patches)
        document.save(self.copy)
