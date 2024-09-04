"""
This file is part of Lynq (elemenom/lynq).

Lynq is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lynq is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lynq. If not, see <https://www.gnu.org/licenses/>.
"""

import os

from typing import Optional
from typing import Any

from lynq import GLOBAL_LOGGER as logger

from lynq.launcher import launch

from lynq._backendutils.app.supportswith import SupportsWithKeyword
from lynq._backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects
from lynq._backendutils.app.supportedtags import supported_tags

from lynq._backendutils.app.appobject import AppObject

class CustomAppObject(AppObject):
    def __init__(self, name: Optional[str], server: Optional[LynqServerOrRelatedObjects] = None) -> None:

        self.server: Any = server
        self.name: str = f"{name}.html"

        self.init_supported_tags(supported_tags)

        self.on_run()

    def on_run(self) -> None:
        self.singular("<!DOCTYPE html>")
        self.singular("<html>")

    def init_supported_tags(self, supported_tags: list[str]) -> None:
        for tag in supported_tags:
            exec(f"self.{tag} = lambda style = None, args = None: self.tag({repr(tag)}, style, args)", {"self": self})

    def tag(self, type_: str, style: Optional[str] = None, args: Optional[str] = None) -> Any:
        from lynq._backendutils.custom.tagobject import CustomTagObject

        return CustomTagObject(self.name.removesuffix(".html"), type_, style, args)
    
    def singular(self, ln: str) -> None:
        with open(self.name, "a") as file:
            file.write(ln + "\n")
    
    def __exit__(self, *_) -> None:
        self.singular("</html>")

        self.pass_to_server()
    
    def pass_to_server(self) -> None:
        if self.server is None:
            logger.error("Cannot pass pebl script to server when no server was provided.")
            raise

        logger.info(f"Passed {self.name} pebl script to {type(self.server).__name__}")

        launch(self.server)

        logger.info("Continuing in pebl app to clear cache.")
        os.remove("index.html")