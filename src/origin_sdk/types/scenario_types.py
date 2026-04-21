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

    Note that while you may be able to create a scenario partially, the values
    required to put it into a launchable state vary based on configuration. If
    you are missing parameters, the service ought to tell you what is missing.

    Notes:
        Field details:

        * ``projectGlobalId``: The ID of the project to create the scenario in.
        * ``name``: The name of the scenario.
        * ``baseScenarioGlobalId``: Required only for non-Aurorean use. The
          "base" scenario you wish to use. This is equivalent to your own
          scenario, or a published AER scenario that you wish to "copy".
        * ``description``: A description for the scenario. Purely for user
          purposes, not used by the system.
        * ``regionGroupCode``: A region group for the scenario. Be aware that
          a region group would be ``AUS``, whereas a region would then be
          ``VIC`` or ``NSW``. For most regions, the region group and its
          three-letter region code are identical.
        * ``useExogifiedInputs``: Equivalent to "Model Determined Capacity"
          being toggled off in the interface. When this is set to ``False``,
          the model automatically builds capacity to support demand. If you
          unset this, you are choosing to take control of the capacity build
          assumptions yourself. Whether these options are available depends on
          the scenario this is based on.
        * ``defaultCurrency``: Should be set automatically once a
          ``regionGroupCode`` is chosen, but can be overridden.
        * ``retentionPolicy``: Internal only.
        * ``scenarioRunType``: Deprecated for external use. External users
          should use ``useExogifiedInputs`` instead. Set
          ``useExogifiedInputs=True`` for MDC off (fixed capacities), or
          ``useExogifiedInputs=False`` for MDC on (model-determined
          capacities).
        * ``modelType``: Internal only. Can be values ``AERES``, ``NODAL``,
          ``REGIONAL``, or ``NETWORK``.
        * ``modelPriceSpikiness``: Used for AUS. Set this to one of the
          ``ModelPriceSpikiness`` enum values if you wish to use the feature.
        * ``years``: Internal only.
        * ``weatherYear``: The weather year for which to simulate
          (half-)hourly profiles, if supported. This should only be used for
          scenarios with fixed capacities and without further edits, for
          example ``useExogifiedInputs=True`` or ``scenarioRunType=FYR``.
        * ``advancedSettings``: Internal only.
    """

    projectGlobalId: str
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
    Regional information object.

    Notes:
        Field details:

        * ``regionCode``: ISO code or similar from the service.
        * ``metaUrl``: URL used to get the meta JSON file for this region's
          downloads.
        * ``dataUrlBase``: URL used as the base to construct a download URL
          for output data.
        * ``__meta_json``: Not provided by the service. This field is
          populated as required by the internal implementation of the
          ``Scenario`` class. Observe this at your own risk.
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
