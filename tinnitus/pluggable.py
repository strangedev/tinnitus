import importlib.util
import threading
from typing import Callable, Any


class Pluggable(object):

    def __init__(self):

        self.__lock = threading.Lock()
        self.__backends = dict({})
        self.__backend = None
        self.__callback = None


    def __add_backend(self, backend: str, module_path: str) -> None:
        with self.__lock:
            spec = importlib.util.spec_from_file_location(backend, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.__backends[backend] = module


    @property
    def backend(self):
        backend = None
        with self.__lock:
            backend = self.__backend
        return backend


    def use_backend(self, backend: str) -> None:
        with self.__lock:
            self.__backend = self.__backends[backend]

            initialized = False

            if hasattr(self.__backend, "initialized"):
                initialized = self.__backend.initialized

            if not initialized:
                self.__backend.init(self.__callback)
                setattr(self.__backend, "initialized", True)


    def set_callback(self, media_end_callback: Callable[[Any], None]) -> None:
        self.__callback = media_end_callback
