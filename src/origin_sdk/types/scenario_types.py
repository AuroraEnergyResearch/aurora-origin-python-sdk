from typing import TypedDict, List, Any, Optional
from enum import Enum


class ScenarioRunStatus(Enum):
    QUEUED = "Queued"
    RUNNING = "Running"
    COMPLETE = "Complete"
    ERRORED = "Errored"
    NOT_LAUNCHED = "NotLaunched"


class ScenarioRunType(Enum):
    MYR_AND_FYR = "MYR_AND_FYR"
    MYR = "MYR"
    FYR = "FYR"


class ScenarioOwner(Enum):
    AURORA_SCENARIO = "AURORA_SCENARIO"
    TENANTED_SCENARIO = "TENANTED_SCENARIO"


class ScenarioTransformStatus(Enum):
    COMPLETE = "Complete"
    ERRORED = "Errored"
    NOT_STARTED = "NotStarted"


class InputTypesSupported(Enum):
    EXOGENOUS_ONLY = "EXOGENOUS_ONLY"
    ENDOGENOUS_ONLY = "ENDOGENOUS_ONLY"
    ENDOGENOUS_AND_EXOGENOUS = "ENDOGENOUS_AND_EXOGENOUS"


class ModelPriceSpikiness(Enum):
    NONE = "None"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class ServerName(Enum):
    AWS = "AWS"
    AZATHOTH = "Azathoth"
    BRYNHILDR = "Brynhildr"
    HASTUR = "Hastur"
    QUETZAL = "Quetzal"
    TATZELWURM = "Tatzelwurm"
    CTHULHU = "Cthulhu"


class RetentionPolicyEnum(Enum):
    SHORT_TERM = "ShortTerm"
    STANDARD = "Standard"
    MIDTERM = "MidTerm"
    LONG_TERM = "LongTerm"
    CENTRAL = "Central"


class AdvancedScenarioSettings(TypedDict):
    baseInputReference: str
    baseInputReferenceType: str
    modelReference: str
    controlFileName: str
    stateFile: str
    quickTry: bool
    retentionPolicy: str
    numIterations: str
    serverName: str
    devTestMode: str
    isHistoricRun: str
    isPriorityRun: str
    moduloOfYearToConfigForFYR: str


class ScenarioSummaryType(TypedDict):
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


class ScenarioType(ScenarioSummaryType):
    defaultCurrency: str
    sensitivity: str
    regions: Any
    baseScenarioGlobalId: str
    runDetails: Any
    appReleaseStatus: Any
    launchedByEmail: str
    userInputReference: str
    inputImportStatus: str
    currencies: Any
    # controlFileList: List[str]
    # weatherYearList: List[int]
