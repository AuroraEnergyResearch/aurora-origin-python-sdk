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
"""

all_scenario_fields = f"""
	{scenario_summary_fields}
	defaultCurrency
	currencies
	sensitivity
	baseScenarioGlobalId
	runDetails
	appReleaseStatus
	baseInputReference
	baseInputReferenceType
	userInputReference
	inputImportStatus
	years
	weatherYear
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