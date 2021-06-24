import numpy

from typing import List

def to_list(obj: object) -> List:
    if isinstance(obj, list):
        return obj
    elif isinstance(obj, numpy.ndarray):
        return obj.tolist()

    # Just try...
    return list(obj)
