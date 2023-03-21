from aurora.origin.client.gql.fragments.scenario import scenario_summary_fields, all_scenario_fields, advanced_settings_fields

get_scenarios = """
query ($filter: ScenarioFilter) {
	getScenarios (filter: $filter) {
		regions
		{all_scenario_fields}
    {advanced_settings_fields}
	}
}  
"""

create_scenario = """
mutation ($scenario: InputScenario!) {
	createScenario (scenario: $scenario) {
		{scenario_summary_fields}
	}
}
"""

update_scenario = """
  mutation ($scenario: UpdateScenarioInput!) {
	updateScenario (scenario: $scenario) {
		{all_scenario_fields}
    {advanced_settings_fields}
	}
}
"""

delete_scenario = """
mutation ($scenarioGlobalId: String!) {
	deleteScenario (scenarioGlobalId: $scenarioGlobalId)
}
"""

launch_scenario = """
mutation ($scenarioGlobalId: String!) {
	launchScenario (scenarioGlobalId: $scenarioGlobalId) {
		{all_scenario_fields}
    {advanced_settings_fields}
	}
}
"""