"""
Utils
"""

import numpy as np


def choose_uint_dtype(arr):
    max_val = arr.max()
    if max_val <= np.iinfo(np.uint8).max:
        return np.uint8
    elif max_val <= np.iinfo(np.uint16).max:
        return np.uint16
    elif max_val <= np.iinfo(np.uint32).max:
        return np.uint32
    else:
        return np.uint64


def delegate_to(module_name, func_name):
    """Crée une méthode qui importe et appelle une fonction d'un autre module."""

    # import functools
    import importlib

    # @functools.wraps(func)  # copie __name__, __doc__, __annotations__, etc.
    def method(self, *args, **kwargs):
        mod = importlib.import_module(module_name, package=__package__)
        func = getattr(mod, func_name)
        return func(self, *args, **kwargs)

    return method
