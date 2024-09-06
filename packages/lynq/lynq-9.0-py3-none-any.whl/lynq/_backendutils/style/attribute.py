from typing import Self, Any

from lynq._backendutils.app.supportswith import SupportsWithKeyword

class StyleAttribute(SupportsWithKeyword):
    def __init__(self, style: Any, tag_name: str) -> None:
        self.style: Any = style

        self.name: str = tag_name

        self.written: str = ""

        self._init_attribute()

    def _init_attribute(self) -> None:
        self._write_line(f"{self.name} " + "{")

    def _write_line(self, contents: str) -> None:
        self.written += f"{contents}\n"

    def add_singular(self, contents: str) -> Self:
        self._write_line(contents)

        return self

    def add_option(self, key: str, value: str) -> Self:
        self._write_line(f"{key}: {value};")

        return self

    def __exit__(self, *_) -> None:
        self.close()

    def back(self) -> Self:
        self._write_line("}")

        return self.style

    def get_written(self) -> str:
        return self.written