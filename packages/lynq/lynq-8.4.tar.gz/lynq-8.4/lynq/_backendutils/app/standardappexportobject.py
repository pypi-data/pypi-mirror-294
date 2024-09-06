from typing import Any, Callable

from lynq._backendutils.app.appobject import AppObject
from lynq._backendutils.app.app import app

from lynq._backendutils.app.supportswith import SupportsWithKeyword

class StandardAppExportObject(SupportsWithKeyword):
    def __init__(self, app_: app, object_: Any = AppObject, *args: Any, **kwargs: Any) -> None:
        self.app: app = app_
        self.object: type[object_] = object_
        self.args: tuple[Any, ...] = args
        self.kwargs: dict[str, Any] = kwargs

    def open(self) -> Any:
        app_object: type[self.object] = self.object(self.app.fn.__name__, self.app)
        try: return self.app.fn(app_object, *self.args, **self.kwargs)
        finally: app_object.pass_to_server()

    def init_postbuilding(self, type_: Callable) -> None:
        self.postb: Any = type_(self.app.fn.__name__, self.app.server)

    def get_object_type(self) -> Any:
        return self.object
    
    def get_app(self) -> app:
        return self.app