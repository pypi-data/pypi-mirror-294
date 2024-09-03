from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from types import ModuleType
from typing import Any
from inspect import getmembers, isclass


def load_module(path: Path) -> ModuleType:
    n = path.name.replace(path.suffix, "")
    s = spec_from_file_location(n, path)
    m = module_from_spec(s)
    s.loader.exec_module(m)
    return m


def get_class_names(module: ModuleType) -> list[str]:
    return [name for name, obj in getmembers(module, isclass) if obj.__module__ == module.__name__]


def load_cls(path: Path, name: str, *args, **kwargs):
    """
    Load a class from a file by its name

    :param path: Path to file containing the class
    :param name: Classname to initialize (if a file contains more than one class
    :param args: Arguments to pass to the constructor
    :param kwargs: Keyword arguments to pass to the constructor
    :return:
    """
    return load_module(path).__dict__[name](*args, **kwargs)


def load_dir(directory: Path, arguments: dict[str, dict[str, Any]]) -> dict:
    """
    Load a directory of modules

    :param directory: Path to load modules from
    :param arguments: Dictionary of arguments for each class by name
    :return:
    """
    r = {}
    for path in directory.iterdir():
        if path.is_file():
            m = load_module(path)
            for name in get_class_names(m):
                if name in arguments.keys():
                    r[name] = load_cls(path, name, *(), **arguments[name])
                else:
                    r[name] = load_cls(path, name)
    return r


__all__ = ['load_cls', 'load_dir']
