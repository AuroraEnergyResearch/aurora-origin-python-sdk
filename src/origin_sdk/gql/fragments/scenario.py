scenario_summary_fields = """
  scenarioGlobalId
  name
  description
  regionGroupCode
  publishType
  publicationDate
  scenarioRunStatus
  scenarioTransformStatus
  inputTypesSupported
  scenarioType
  scenarioRunType
  useExogifiedInputs
  projectGlobalId
  scenarioInputsAvailable
  scenarioOutputsAvailable
  scenarioLaunchable
  baseInputReference
  baseInputReferenceType
  runStartedAtUTC
  runCompletedAtUTC
  launchedByUserName
  modelPriceSpikiness
  years
  weatherYear
  supportsExogenousInputs
  lastUpdated
  advancedSettings {
    modelReference
    controlFileName
  }
  runDetails
"""

all_scenario_fields = f"""
  {scenario_summary_fields}
  defaultCurrency
  sensitivity
  regions
  baseScenarioGlobalId
  appReleaseStatus
  launchedByEmail
  userInputReference
  inputImportStatus
  currencies
"""

advanced_settings_fields = """
  advancedSettings {
    modelReference
    controlFileName
    stateFile
    quickTry
    retentionPolicy
    numIterations
    serverName
    isHistoricRun
    isPriorityRun
    moduloOfYearToConfigForFYR
  }
"""
