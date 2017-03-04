import os
import importlib.util

from core.settings import BASE_DIR


def load(name):
    for fn in next(os.walk(BASE_DIR))[1]:
        try:
            spec = importlib.util.find_spec('.'.join((fn, name)), name)
            if spec:
                spec.loader.exec_module(importlib.util.module_from_spec(spec))
        except ModuleNotFoundError:
            pass


def import_module(path):
    return (
        lambda package, module:
            getattr(importlib.import_module(package, module), module)
    )(*path.rsplit('.', 1))


def import_modules(resources):
    return map(import_module, resources)
