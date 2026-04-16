import importlib.util
import importlib.machinery
import os
import sys


def find_module(name, path=None):
    if path is None:
        spec = importlib.util.find_spec(name)
    else:
        spec = importlib.util.find_spec(name, path)

    if spec is None or spec.origin is None:
        raise ImportError(f"No module named {name}")

    loader = spec.loader
    pathname = spec.origin
    description = None
    return loader, os.path.dirname(pathname), description


def load_module(name, file, pathname, description=None):
    if name in sys.modules:
        return sys.modules[name]

    spec = importlib.util.spec_from_file_location(name, pathname)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    if spec.loader is not None:
        spec.loader.exec_module(module)
    return module
