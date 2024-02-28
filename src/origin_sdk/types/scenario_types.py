"""
The scenario_types module contains type hinting and can be useful when trying to
understand what options you have when interacting with functions, or what
outputs to expect from queries. Enums are available in
[scenario_enums](/docs/origin_sdk/types/scenario_enums) for import and usage.
"""

from typing import Dict, TypedDict, List, Any, Optional
from origin_sdk.types.scenario_enums import (
    ScenarioRunStatus,
    ScenarioRunType,
    ScenarioOwner,
    ScenarioTransformStatus,
    InputTypesSupported,
    ModelPriceSpikiness,
)


class AdvancedScenarioSettings(TypedDict):
    baseInputReference: Optional[str]
    baseInputReferenceType: Optional[str]
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


class InputScenario(TypedDict):
    """
    Interface for creating or updating scenarios. Note that while you may be
    able to create a scenario partially, the values required to put it into a
    launchable state varies based on configuration. If you are missing
    parameters, the service ought to tell you what is missing.

    Attributes:

        projectGlobalId (string): The ID of the project to create the scenario
        in
        name (string): The name of the scenario
        baseScenarioGlobalId (string): **Required only for non-Aurorean use.** The
            "base" scenario you wish to use. This is equivalent to your own
            scenario, or a published AER scenario that you wish to "copy".
        description (optional, string): A description for the scenario. Purely for user
            purposes, not used by the system.
        regionGroupCode (optional, string): A region group for the scenario. Be aware
            that a "regionGroup" would be AUS, whereas a "region" would then be
            "VIC" or "NSW". For most regions, the "regionGroup" and it's three
            letter region code are identical.
        useExogifiedInputs (boolean): A true value here is equivalent to the
            "Model Determined Capacity" toggled off in the interface. When this
            is set to false, the model automatically builds capacity to support
            demand. If you unselect this, you are choosing to take control of
            defining the capacity build assumptions (this runs much more
            quickly). Whether these options are available, depends on the
            scenario this is based on.
        defaultCurrency (optional, string): Should be set automatically once a
            `regionGroupCode` is chosen, but can be overridden
        retentionPolicy (optional, string): Internal only.
        scenarioRunType (optional, ScenarioRunType): Internal only. Can be values `MYR`, `FYR` or
            `MYR_AND_FYR`. Non-Auroreans should look to using the
            `useExogifiedInputs` flag over the scenarioRunType. The behaviour
            between the two differs slightly for a better Origin experience.
        modelPriceSpikiness (optional, ModelPriceSpikiness): Used for AUS, set
            this to one of the ModelPriceSpikiness enum values if you wish to
            use the feature.
        years (optional, List[int]): Internal only.
        weatherYear (optional, int): Internal only, but a form of this coming
            soon for non-Aurorean usage.
        advancedSettings (optional, AdvancedScenarioSettings): Internal only.
    """

    projectGlobalId: str
    name: str
    baseScenarioGlobalId: Optional[str]
    description: Optional[str]
    regionGroupCode: Optional[str]
    scenarioRunType: Optional[ScenarioRunType]
    useExogifiedInputs: Optional[bool]
    defaultCurrency: Optional[str]
    retentionPolicy: Optional[str]
    modelPriceSpikiness: Optional[ModelPriceSpikiness]
    preserveBaseScenarioTransformations: Optional[bool]
    userInputReference: Optional[str]
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


class RegionDict(TypedDict):
    """
    Regional information object.

    Attributes:
        regionCode (String): ISO code or similar from the service
        metaUrl (String): URL used to get the meta json file for this region's downloads
        dataUrlBase (String): URL used as the base to construct a download URL
        for output data
        __meta_json (Optional): Not provided by the service. This field is
        populated as required by internal implementation of the Scenario class.
        Observe this at your own risk.
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
    runDetails: Any
    appReleaseStatus: Any
    launchedByEmail: str
    userInputReference: str
    inputImportStatus: str
    currencies: Any
    # controlFileList: List[str]
    # weatherYearList: List[int]
