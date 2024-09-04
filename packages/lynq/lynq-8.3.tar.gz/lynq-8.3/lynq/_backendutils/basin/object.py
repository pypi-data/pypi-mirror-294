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

from typing import Self
from typing import Any

from lynq._backendutils.basin.basinreturnobject import BasinReturnObject

class BasinObject:
    def __init__(self, path: str | None = None) -> None:
        self.path: str = path or "config.bsn"

    def set_path(self, path: str | None = None) -> Self:
        self.path = path or "config.bsn"

        return self
    
    def read_whole(self) -> BasinReturnObject:
        o: BasinReturnObject = {}

        with open(self.path) as file:
            for ln in [i.strip() for i in file.read().split("\n")]:
                print(file.read())
                k, v = ln.strip().split("=", 1)

                o.update({k.strip(): eval(v.strip())})

        return o
    
    def read_line(self, number: int) -> BasinReturnObject:
        with open(self.path) as file:
            c: str = file.readline(number).strip()
            return {c[0]: eval(c[1])}