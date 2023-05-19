from typing import TypedDict, Any
from enum import Enum


class ModelVariableType(Enum):
    ENDOGENOUS = "endogenous"
    EXOGENOUS = "exogenous"


class TransformType(Enum):
    PERCENTAGE = "Percentage"
    DELTA = "Delta"
    ABSOLUTE = "Absolute"


class TransformInput(TypedDict):
    type: TransformType
    value: Any


class Transform(TypedDict):
    transform: TransformInput
    year: int
