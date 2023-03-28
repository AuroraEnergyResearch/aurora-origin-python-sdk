from typing import Optional, TypedDict, List
from origin_sdk.types.scenario_types import ScenarioSummaryType


class ProjectSummaryType(TypedDict):
    projectGlobalId: str
    name: str
    description: str
    productId: str
    productName: Optional[str]
    isProjectPinned: bool


class ProjectType(ProjectSummaryType):
    scenarios: List[ScenarioSummaryType]