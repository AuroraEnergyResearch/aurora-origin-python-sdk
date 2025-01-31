from enum import Enum


class ScenarioRunStatus(Enum):
    QUEUED = "Queued"
    RUNNING = "Running"
    COMPLETE = "Complete"
    ERRORED = "Errored"
    NOT_LAUNCHED = "NotLaunched"


class ScenarioRunType(Enum):
    """
    Internal only. Used to set a `scenarioRunType`.
    """

    MYR_AND_FYR = "MYR_AND_FYR"
    MYR = "MYR"
    FYR = "FYR"
    NODAL = "NODAL"
    NODAL_PLACEMENT = "NODAL_PLACEMENT"
    REGIONAL_MYR = "REGIONAL_MYR"
    REGIONAL_FYR = "REGIONAL_FYR"
    REGIONAL_MYR_AND_FYR = "REGIONAL_MYR_AND_FYR"
    NETWORK = "NETWORK"


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
    """Used to set a Model Price Spikiness on a scenario that implements this
    feature, typically from the AUS region."""

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
