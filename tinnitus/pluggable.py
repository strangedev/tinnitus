import importlib.util
import os
import threading
from pathlib import Path
from typing import Callable, Any

import tinnitus


class Pluggable(object):

    def __init__(self):

        self.__lock = threading.Lock()
        self.__backends = dict({})
        self.__backend = None
        self.__callback = None

        self.__find_plugins()


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


    def __find_plugins(self):

        plugin_path = os.path.join(Path(os.path.join(*Path(tinnitus.__file__).parts[0:-2])).as_posix(), 'plugins')

        for dirname in os.listdir(plugin_path):
            absolute_path = os.path.join(plugin_path, dirname)

            if '__init__.py' not in os.listdir(absolute_path):
                continue

            path_to_init = os.path.join(absolute_path, '__init__.py')

            spec = importlib.util.spec_from_file_location(dirname, path_to_init)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            is_backend = False

            try:
                is_backend = all([
                    hasattr(module, "set_mrl"), callable(getattr(module, "set_mrl")),
                    hasattr(module, "init"), callable(getattr(module, "init")),
                    hasattr(module, "play"), callable(getattr(module, "play")),
                    hasattr(module, "pause"), callable(getattr(module, "pause")),
                    hasattr(module, "stop"), callable(getattr(module, "stop"))])

            except Exception:
                pass

            if is_backend:
                with self.__lock:
                    self.__backends[dirname] = module
