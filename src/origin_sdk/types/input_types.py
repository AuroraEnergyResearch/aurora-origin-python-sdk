from typing import Annotated, Optional, TypedDict, Any, List, Dict, Union
from enum import Enum


class ModelVariableType(Enum):
    ENDOGENOUS = "endogenous"
    EXOGENOUS = "exogenous"


class VariableValues(TypedDict):
    original: Any
    validationWarnings: List[str]
    validationErrors: List[str]


class TransformType(Enum):
    PERCENTAGE = "Percentage"
    DELTA = "Delta"
    ABSOLUTE = "Absolute"


class TransformInput(TypedDict):
    type: TransformType
    value: Any


class Transform(TypedDict, total=False):
    transform: TransformInput
    year: int
    month: int


class VariableValuesWithTransform(VariableValues):
    transform: TransformInput


class TechGroupingSubTechs(TypedDict):
    subTechnologiesExogenous: List[str]
    subTechnologiesEndogenous: List[str]


class TechGroupingSubregion(TechGroupingSubTechs):
    subsidies: List[str]


class TechGrouping(TechGroupingSubTechs):
    subRegions: Dict[str, TechGroupingSubregion]


TechnologyNames = Annotated[
    Dict[str, Dict[str, TechGrouping]],
    """Structure used for complex technology groupings in Origin""",
]


class InputsSessionMeta(TypedDict):
    sessionId: str
    tenant: str


class InputsSessionDataGroup(TypedDict):
    reference: str
    referenceType: str
    productRegion: Optional[str]
    loading: bool
    loadingRequest: dict


class InputsCurrencyInformation(TypedDict):
    name: str
    currencyCode: str
    year: int
    currencyBaseCode: str
    inflationFactor: float
    useExchangeRate: int


class InputsSessionEnabledRegion(TypedDict):
    code: str
    isFocusRegion: bool
    isEndogenous: bool
    isMainRegion: bool
    hasCapacityMarket: bool


class InputsSessionProductRegionInfo(TypedDict):
    code: str
    enabledRegions: List[InputsSessionEnabledRegion]


class InputsSessionTransform(TypedDict):
    updateParameters: Any
    reason: str
    steps: List[Any]


class InputsSession(TypedDict):
    meta: InputsSessionMeta
    dataGroups: Dict[str, InputsSessionDataGroup]
    currencyInformation: InputsCurrencyInformation
    defaultCurrency: str
    productRegionInformation: InputsSessionProductRegionInfo
    dataGroupEligibility: Dict[str, Union[bool, str]]
    modelMaxYear: int
    modelMinYear: int
    transforms: List[InputsSessionTransform]


class InputsDemandVariables(TypedDict):
    year: int
    totalDemand: VariableValuesWithTransform
    baseDemand: VariableValuesWithTransform


class YearlyValue(TypedDict):
    year: int


YearlyVariables = Union[YearlyValue, dict[str, VariableValuesWithTransform]]


class InputsDemandTechnologies(TypedDict):
    region: str
    technology: str
    originTechnology: str
    variables: List[YearlyVariables]


class InputsDemand(TypedDict):
    region: str
    peakLoadDemand: float
    variables: List[YearlyVariables]
    technologies: List[YearlyVariables]


class InputsDemandFilter(TypedDict):
    region: str
    regions: List[str]
