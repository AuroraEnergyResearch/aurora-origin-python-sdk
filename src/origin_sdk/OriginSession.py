from typing import Any, List, Optional, TypedDict
import logging
import origin_sdk.gql.queries.project_queries as project_query
import origin_sdk.gql.queries.scenario_queries as scenario_query
import origin_sdk.gql.queries.input_queries as input_query

from core.api import APISession
from origin_sdk.types.project_types import InputProject, ProjectSummaryType, ProjectType
from origin_sdk.types.scenario_types import (
    InputScenario,
    ScenarioSummaryType,
    ScenarioType,
)
from origin_sdk.types.input_types import ModelVariableType, Transform

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


class OriginSessionConfig(TypedDict, total=False):
    token: str
    scenario_base_url: str
    inputs_base_url: str


class OriginSession(APISession):
    """Manage access to the Origin API.

    By default the session will connect to the production Origin API endpoint.
    This can be overridden by passing the base_url into the constructor or by
    setting the above environment variables for BASE_URLs. This feature is for
    internal use only.

    The authentication token is read from the user's home directory
    *$home/.aurora-api-key* e.g. *C:/Users/Joe Bloggs/.aurora-api-key*. This can
    be overridden by passing the token into the constructor or by setting the
    environment variable *AURORA_API_KEY*.

    Args:
        token (string, optional): Override the api authentication token used for
        API access. Defaults to None.
        scenario_base_url (string, optional): Override the scenario service base url
        inputs_base_url (string, optional): Override the model inputs service base url
    """

    inputs_config_cache: Any = None

    def __init__(self, config: OriginSessionConfig = {}):
        super().__init__(config.get("token"))
        self.scenario_service_url = self._get_base_url(
            default_url=AURORA_ORIGIN_SCENARIO_PRODUCTION_ENDPOINT,
            base_url=config.get("scenario_base_url"),
            environment_variable=AURORA_ORIGIN_SCENARIO_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME,
        )
        self.scenario_service_graphql_url = f"{self.scenario_service_url}/v1/graphql"
        self.inputs_service_url = self._get_base_url(
            default_url=AURORA_ORIGIN_INPUTS_PRODUCTION_ENDPOINT,
            base_url=config.get("inputs_base_url"),
            environment_variable=AURORA_ORIGIN_INPUTS_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME,
        )
        self.inputs_service_graphql_url = f"{self.inputs_service_url}/v1/graphql"

    def __getstate__(self):
        state = self.__dict__.copy()

        # Remove the sensitive token information
        state["token"] = None

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Re-initialise the token, there is no realistic way
        # to allow the user to inject a token in the unpickle
        self.token = self._get_token(self.token)

    def get_aurora_scenarios(
        self, region: Optional[str] = None
    ) -> List[ScenarioSummaryType]:
        """
        Gets a list of all published Aurora scenarios.

        Args:
            region (string, optional) - A regional filter. We accept three
            letter ISO codes where appropriate. If in doubt as to which code to
            use for a region (e.g. Iberia), you can check the Origin URL while
            browsing the platform. You will see something like
            ".../launcher/aer/<REGION>"

        Returns:
            List[ScenarioSummaryType]
        """
        url = f"{self.scenario_service_graphql_url}"
        variables = {
            "filter": {
                **({"regionGroupCode": region} if region is not None else {}),
                # **(query_filter if query_filter is not None else {}),
                "scenarioType": "AURORA_SCENARIO",
            }
        }
        return self._graphql_request(url, scenario_query.get_scenarios, variables)

    # Only support querying based on id, region and type currently
    # def get_scenarios(self, query_filter):
    #     """ """
    #     url = f"{self.scenario_service_graphql_url}"
    #     variables = {"filter": {**query_filter, "scenarioType": "TENANTED_SCENARIO"}}
    #     return self._graphql_request(url, scenario_query.get_scenarios,
    #     variables)

    def get_scenario_by_id(self, scenario_id: str) -> ScenarioType:
        """
        Get a single scenario by it's ID.

        Args:
            scenario_id (string) - The ID of the scenario

        Returns:
            ScenarioType
        """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"filter": {"scenarioGlobalId": scenario_id}}
        return self._graphql_request(
            url, scenario_query.get_scenario_details, variables
        )[0]

    def create_scenario(self, scenario: InputScenario) -> ScenarioType:
        """
        Creates a new scenario

        Args:
            scenario (InputScenario) -
        """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"scenario": scenario}
        return self._graphql_request(url, scenario_query.create_scenario, variables)

    def update_scenario(self, scenario_update) -> ScenarioType:
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"scenario": scenario_update}
        return self._graphql_request(url, scenario_query.update_scenario, variables)

    def delete_scenario(self, scenario_id: str):
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"scenarioGlobalId": scenario_id}
        return self._graphql_request(url, scenario_query.delete_scenario, variables)

    def launch_scenario(self, scenario_id: str) -> ScenarioType:
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"scenarioGlobalId": scenario_id}
        return self._graphql_request(url, scenario_query.launch_scenario, variables)

    def get_projects(self) -> List[ProjectSummaryType]:
        """ """
        url = f"{self.scenario_service_graphql_url}"
        return self._graphql_request(url, project_query.get_projects)

    def get_project(self, project_id: str) -> ProjectType:
        """ """
        url = f"{self.scenario_service_graphql_url}"
        variables = {"projectId": project_id}
        return self._graphql_request(url, project_query.get_project, variables)

    def create_project(self, project: InputProject) -> ProjectSummaryType:
        """"""
        url = f"{self.scenario_service_graphql_url}"
        variables = {"project": project}
        return self._graphql_request(url, project_query.create_project, variables)

    def update_project(self, project_update) -> ProjectSummaryType:
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

    def get_meta_json(self, meta_url: str):
        """"""
        url = f"{self.scenario_service_url}/{meta_url}"
        return self._get_request(url)

    def get_inputs_session(self, scenario_id: str):
        """Gets the inputs instance information, as well as rehydrating all the
        data if required"""
        url = f"{self.inputs_service_graphql_url}"
        variables = {"sessionId": scenario_id}
        return self._graphql_request(
            url, input_query.get_session_information_gql, variables
        )

    def get_inputs_config(self):
        if self.inputs_config_cache is None:
            url = self.inputs_service_graphql_url
            self.inputs_config_cache = self._graphql_request(
                url, input_query.get_config_gql
            )
        return self.inputs_config_cache

    def get_technology_names(self, scenario_id: str):
        """"""
        url = f"{self.inputs_service_graphql_url}"
        variables = {"sessionId": scenario_id}
        return self._graphql_request(
            url, input_query.get_technology_names_gql, variables
        )

    def get_technology(
        self,
        scenario_id: str,
        technology_name: str,
        region: str,
        subregion: Optional[str] = None,
        exogenous_sub_technology: Optional[str] = None,
        subsidy: Optional[str] = None,
        endogenous_sub_technology: Optional[str] = None,
    ):
        """"""
        url = f"{self.inputs_service_graphql_url}"
        variables = {
            "sessionId": scenario_id,
            "techName": technology_name,
            "region": region,
            "subregion": subregion,
            "exoSubTechnology": exogenous_sub_technology,
            "subsidy": subsidy,
            "endoSubTechnology": endogenous_sub_technology,
        }
        config = self.get_inputs_config().get("technology")
        return self._graphql_request(
            url, input_query.get_technology_gql(config), variables
        )

    def update_technology_endogenous(
        self,
        scenario_id: str,
        technology_name: str,
        parameter: str,
        transform: List[Transform],
        region: str,
        sub_region: Optional[str] = None,
        sub_technology: Optional[str] = None,
    ):
        url = f"{self.inputs_service_graphql_url}"
        variables = {
            "sessionId": scenario_id,
            "parameter": parameter,
            "tx": transform,
            "name": technology_name,
            "region": region,
            "subRegion": sub_region,
            "subTechnology": sub_technology,
        }

        config = self.get_inputs_config().get("technology")

        return self._graphql_request(
            url, input_query.update_endo_technology_gql(config), variables
        )
