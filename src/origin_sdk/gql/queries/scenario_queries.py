from origin_sdk.gql.fragments.scenario import (
    scenario_summary_fields,
    all_scenario_fields,
    advanced_settings_fields,
)

get_scenarios = f"""
query ($filter: ScenarioFilter) {{
  getScenarios (filter: $filter) {{
    regions
    {scenario_summary_fields}
  }}
}}
"""

get_scenario_details = f"""
query ($filter: ScenarioFilter) {{
  getScenarios (filter: $filter) {{
    {all_scenario_fields}
    {advanced_settings_fields}
  }}
}}
"""

create_scenario = f"""
mutation ($scenario: InputScenario!) {{
  createScenario (scenario: $scenario) {{
    {all_scenario_fields}
    {advanced_settings_fields}
  }}
}}
"""

update_scenario = f"""
  mutation ($scenario: UpdateScenarioInput!) {{
  updateScenario (scenario: $scenario) {{
    {all_scenario_fields}
    {advanced_settings_fields}
  }}
}}
"""

delete_scenario = """
mutation ($scenarioGlobalId: String!) {
  deleteScenario (scenarioGlobalId: $scenarioGlobalId)
}
"""

launch_scenario = f"""
mutation ($scenarioGlobalId: String!) {{
  launchScenario (scenarioGlobalId: $scenarioGlobalId) {{
    {all_scenario_fields}
    {advanced_settings_fields}
  }}
}}
"""

get_weather_years = f"""
query ($scenarioGlobalId: String!) {{
    getWeatherYearList(scenarioGlobalId: $scenarioGlobalId) {{
        years
    }}
}}
"""
