from typing import Optional, Callable

from lynq._backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects

from lynq._backendutils.style.attribute import StyleAttribute

class StyledAppAttachment:
    def __init__(self, path: Optional[str] = None) -> None:
        self.path: str | None = path

        self.write_later: str = ""
        self.attributes: list[StyleAttribute] = []

    def close(self, path: Optional[str] = None) -> None:
        self.path = path or self.path

        for attribute in self.attributes:
            self._write_attrib_contents(attribute)

        self._init_file(path, self.write_later)

    def _init_file(self, path: Optional[str] = None, write: Optional[str] = None) -> None:
        with open((self.path or (path or "index.css")), "w") as file:
            file.write(write or "")

    def add_attribute(self, key: str) -> StyleAttribute:
        attribute: StyleAttribute = StyleAttribute(self, key)

        self.attributes.append(attribute)

        return attribute
    
    def _write_attrib_contents(self, attribute: StyleAttribute) -> None:
        self.write_later += f"{attribute.get_written()}\n"

    def set_path(self, path: str) -> None:
        self.path = path