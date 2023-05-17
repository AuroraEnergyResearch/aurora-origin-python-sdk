from typing import Annotated, Optional, TypedDict, Any, List, Dict, Union
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


class InputsSession(TypedDict):
    meta: InputsSessionMeta
    dataGroups: Dict[str, InputsSessionDataGroup]
    currencyInformation: InputsCurrencyInformation
    defaultCurrency: str
    productRegionInformation: InputsSessionProductRegionInfo
    dataGroupEligibility: Dict[str, Union[bool, str]]
