from typing import Optional
import logging
import origin_sdk.gql.queries.project as project_query
import origin_sdk.gql.queries.scenario as scenario_query
from core.api_session import APISession

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

AURORA_ORIGIN_SCENARIO_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME = (
    "AURORA_ORIGIN_SCENARIO_API_BASE_URL"
)
AURORA_ORIGIN_INPUTS_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME = (
    "AURORA_ORIGIN_INPUTS_API_BASE_URL"
)
AURORA_ORIGIN_SCENARIO_PRODUCTION_ENDPOINT = "https://api.auroraer.com/scenarioExplr"
AURORA_ORIGIN_SCENARIO_STAGE_ENDPOINT = "https://api-staging.auroraer.com/scenarioExplr"
AURORA_ORIGIN_INPUTS_PRODUCTION_ENDPOINT = "https://app.auroraer.com/modelInputs"
AURORA_ORIGIN_INPUTS_STAGE_ENDPOINT = "https://app-staging.auroraer.com/modelInputs"


class OriginSession(APISession):
    """Manage access to the Origin API.

    By default the session will connect to the production Origin API endpoint.
    This can be overridden by passing the base_url into the constructor or by
    setting the above environment variables for BASE_URLs. This feature is for
    internal use only.

    The authentication token is read from the users home directory
    *$home/.aurora-api-key* e.g. *C:/Users/Joe Bloggs/.aurora-api-key*. This can
    be overridden by passing the token into the constructor or by setting the
    environment variable *AURORA_API_KEY*.

    Args:
        token (string, optional): Override the api authentication token used for
        API access. Defaults to None.
        scenario_base_url (string, optional): Override the scenario service base url
        inputs_base_url (string, optional): Override the model inputs service base url
    """

    def __init__(
        self,
        token=None,
        scenario_base_url: Optional[str] = None,
        inputs_base_url: Optional[str] = None,
    ):
        super().__init__(token)
        self.scenario_service_url = self._get_base_url(
            default_url=AURORA_ORIGIN_SCENARIO_PRODUCTION_ENDPOINT,
            base_url=scenario_base_url,
            environment_variable=AURORA_ORIGIN_SCENARIO_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME,
        )
        self.scenario_service_graphql_url = f"{self.scenario_service_url}/v1/graphql"
        self.inputs_service_url = self._get_base_url(
            default_url=AURORA_ORIGIN_INPUTS_PRODUCTION_ENDPOINT,
            base_url=inputs_base_url,
            environment_variable=AURORA_ORIGIN_INPUTS_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME,
        )
        self.inputs_service_graphql_url = f"{self.inputs_service_url}/v1/graphql"

    def get_aurora_scenarios(self, region: Optional[str] = None):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {
            "filter": {
                **({"regionGroupCode": region} if region is not None else {}),
                "scenarioType": "AURORA_SCENARIO",
            }
        }
        return self._graphql_request(url, scenario_query.get_scenarios, variables)

    def get_scenarios(self, query_filter):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"filter": {**query_filter, "scenarioType": "TENANTED_SCENARIO"}}
        return self._graphql_request(url, scenario_query.get_scenarios, variables)

    def get_scenario_by_id(self, scenario_id: str):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"filter": {"scenarioGlobalId": scenario_id}}
        return self._graphql_request(
            url, scenario_query.get_scenario_details, variables
        )

    def create_scenario(self, scenario):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"scenario": scenario}
        return self._graphql_request(url, scenario_query.create_scenario, variables)

    def update_scenario(self, scenario_update):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"scenario": scenario_update}
        return self._graphql_request(url, scenario_query.update_scenario, variables)

    def delete_scenario(self, scenario_id: str):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"scenarioGlobalId": scenario_id}
        return self._graphql_request(url, scenario_query.delete_scenario, variables)

    def launch_scenario(self, scenario_id: str):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"scenarioGlobalId": scenario_id}
        return self._graphql_request(url, scenario_query.launch_scenario, variables)

    def get_projects(self):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {}
        return self._graphql_request(url, project_query.get_projects, variables)

    def get_project(self, project_id: str):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"projectId": project_id}
        return self._graphql_request(url, project_query.get_project, variables)

    def create_project(self, project):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"project": project}
        return self._graphql_request(url, project_query.create_project, variables)

    def update_project(self, project_update):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"project": project_update}
        return self._graphql_request(url, project_query.update_project, variables)

    def delete_project(self, project_id):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"projectGlobalId": project_id}
        return self._graphql_request(url, project_query.delete_project, variables)

    def pin_project(self, project_id):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"projectGlobalId": project_id}
        return self._graphql_request(url, project_query.pin_project, variables)

    def unpin_project(self, project_id):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"projectGlobalId": project_id}
        return self._graphql_request(url, project_query.unpin_project, variables)
