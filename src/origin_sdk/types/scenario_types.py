"""
The scenario_types module contains type hinting and can be useful when trying to
understand what options you have when interacting with functions, or what
outputs to expect from queries. Related enums are available in the
``origin_sdk.types.scenario_enums`` module.
"""

from typing import Dict, TypedDict, List, Any, Optional
from origin_sdk.types.scenario_enums import (
    ScenarioRunStatus,
    ScenarioRunType,
    ScenarioOwner,
    ScenarioTransformStatus,
    InputTypesSupported,
    ModelPriceSpikiness,
    ModelType,
)


class AdvancedScenarioSettings(TypedDict):
    baseInputReference: Optional[str]
    baseInputReferenceType: Optional[str]
    baseInputRepository: Optional[str]
    modelReference: Optional[str]
    controlFileName: Optional[str]
    stateFile: Optional[str]
    quickTry: Optional[bool]
    retentionPolicy: Optional[str]
    numIterations: Optional[str]
    serverName: Optional[str]
    devTestMode: Optional[str]
    isHistoricRun: Optional[str]
    isPriorityRun: Optional[str]
    moduloOfYearToConfigForFYR: Optional[str]
    originMarketScenarioGlobalId: Optional[str]
    simulationMode: Optional[str]


class InputScenario(TypedDict):
    """
    Interface for creating or updating scenarios.

    Some fields are only required for specific scenario configurations. The
    service will report which fields are missing for a given launch state.
    """

    projectGlobalId: str
    name: str
    baseScenarioGlobalId: Optional[str]
    description: Optional[str]
    regionGroupCode: Optional[str]
    scenarioRunType: Optional[ScenarioRunType]
    modelType: Optional[ModelType]
    useExogifiedInputs: Optional[bool]
    defaultCurrency: Optional[str]
    retentionPolicy: Optional[str]
    modelPriceSpikiness: Optional[ModelPriceSpikiness]
    preserveBaseScenarioTransformations: Optional[bool]
    userInputReference: Optional[str]
    userInputRepository: Optional[str]
    years: Optional[List[int]]
    weatherYear: Optional[int]
    advancedSettings: Optional[AdvancedScenarioSettings]


class ScenarioSummaryType(TypedDict):
    """Dictionary received when requesting a list of scenarios"""

    scenarioGlobalId: str
    name: str
    description: str
    regionGroupCode: str
    publishType: str
    publicationDate: str
    scenarioRunStatus: ScenarioRunStatus
    scenarioType: ScenarioOwner
    advancedSettings: AdvancedScenarioSettings
    projectGlobalId: str
    scenarioRunType: ScenarioRunType
    supportsExogenousInputs: str
    inputTypesSupported: InputTypesSupported
    lastUpdated: str
    scenarioInputsAvailable: bool
    scenarioOutputsAvailable: bool
    scenarioLaunchable: bool
    runStartedAtUTC: str
    runCompletedAtUTC: str
    launchedByUserName: str
    modelPriceSpikiness: ModelPriceSpikiness
    baseInputReference: str
    baseInputReferenceType: str
    years: List[int]
    scenarioTransformStatus: ScenarioTransformStatus
    weatherYear: Optional[int]
    useExogifiedInputs: bool
    runDetails: Any


class RegionDict(TypedDict):
    """
    Regional download metadata returned by the service.
    """

    regionCode: str
    metaUrl: str
    dataUrlBase: str
    __meta_json: Optional[Any]


class ScenarioType(ScenarioSummaryType):
    """Extended scenario details received when requesting a single scenario"""

    defaultCurrency: str
    sensitivity: str
    regions: Dict[str, RegionDict]
    baseScenarioGlobalId: str
    appReleaseStatus: Any
    launchedByEmail: str
    userInputReference: str
    userInputRepository: str
    inputImportStatus: str
    currencies: Any
    # controlFileList: List[str]
    # weatherYearList: List[int]
