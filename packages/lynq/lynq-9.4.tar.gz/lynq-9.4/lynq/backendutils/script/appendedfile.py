from typing import Optional

from lynq import GLOBAL_LOGGER as logger

class AppendedFile:
    def __init__(self):
        self.path: str | None = None

    def init_file(self, path: str) -> None:
        self.path = path

        self.write()

    def write(self, cont: Optional[str] = None) -> None:
        if not self.path:
            logger.fatal("Cannot write to file appendant when file was not initialised.")
            exit(1)

        with open(self.path, "a") as file:
            file.write((cont or "") + "\n")

    def read(self) -> str:
        if not self.path:
            logger.fatal("Cannot read from file appendant when file was not initialised.")
            exit(1)

        with open(self.path) as file:
            return file.read()