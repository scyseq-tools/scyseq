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
