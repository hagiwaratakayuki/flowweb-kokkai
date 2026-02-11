from typing import Callable, Dict

from numpy import ndarray


type NounVectors = Dict[any, ndarray]
type ProjectFunction = Callable[[NounVectors], NounVectors]
