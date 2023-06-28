from typing import Optional, TypedDict, List, Union
from origin_sdk.types.scenario_types import ScenarioSummaryType


class InputProject(TypedDict):
    name: str
    description: Optional[str]
    productId: Optional[Union[int, str]]


class ProjectSummaryType(TypedDict):
    projectGlobalId: str
    name: str
    description: str
    productId: str
    productName: Optional[str]
    isProjectPinned: bool


class ProjectType(ProjectSummaryType):
    scenarios: List[ScenarioSummaryType]
