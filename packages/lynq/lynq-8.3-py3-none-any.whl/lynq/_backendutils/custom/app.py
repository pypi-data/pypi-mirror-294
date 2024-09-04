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

from typing import Callable, Any, Optional

from lynq._backendutils.app.app import app
from lynq._backendutils.lynq.lynqserverorrelated import LynqServerOrRelatedObjects

class customapp(app):
    def __init__(self, object_: Any, server: Optional[LynqServerOrRelatedObjects] = None) -> None:
        super().__init__(server)

        self.object: Any = object_

    def export_standard(self, fn: Callable) -> Callable:
        self.fn: Callable = fn

        from lynq._backendutils.app.standardappexportobject import StandardAppExportObject

        return lambda *args, **kwargs: StandardAppExportObject(self, *args, object_=self.object, **kwargs)
    
    def export_direct(self, fn: Callable) -> None:
        app: type[self.object] = self.object(fn.__name__, self.app.server)
        try: return fn(app, *self.args, **self.kwargs)
        finally: app.pass_to_server()
    
    def export_nopass(self, fn: Callable) -> None:
        app: type[self.object] = self.object(self.app.fn.__name__, self.app.server)
        return self.app.fn(app, *self.args, **self.kwargs)