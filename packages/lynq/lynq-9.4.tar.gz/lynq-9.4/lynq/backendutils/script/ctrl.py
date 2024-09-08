from contextlib import contextmanager

from lynq.backendutils.script.appendedfile import AppendedFile

class CTRLScript(AppendedFile):
    def __init__(self, name: str):
        super().__init__()

        self.init_file(f"{name}.js")

    @contextmanager
    def function(self, name: str, *args: str) -> None:
        self.write(f"function {name}({", ".join(list(args))}) ""{")

        yield

        self.write("}")

    @contextmanager
    def export_function(self, name: str, *args: str) -> None:
        self.write(f"function {name}({", ".join(list(args))}) ""{")

        yield

        self.write("}")

    def line(self, ln: str) -> None:
        self.write(f"{ln};")

    def import_module(self, name: str) -> None:
        self.write(f"import {name};")

    def let(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"let {kwarg[0]} = {kwarg[1]};")

    def set(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"{kwarg[0]} = {kwarg[1]};")

    def increment(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"{kwarg[0]} += {kwarg[1]};")

    def decrement(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"{kwarg[0]} -= {kwarg[1]};")

    def multiply(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"{kwarg[0]} *= {kwarg[1]};")

    def divide(self, **kwargs: str) -> None:
        for kwarg in list(kwargs.items()):
            self.write(f"{kwarg[0]} /= {kwarg[1]};")