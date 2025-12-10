from functools import lru_cache
from json import dumps
from textwrap import dedent
from time import sleep
from collections import defaultdict
from typing import Any, List, Optional, TypedDict, Union, Dict
import logging
import origin_sdk.gql.queries.project_queries as project_query
import origin_sdk.gql.queries.scenario_queries as scenario_query
import origin_sdk.gql.queries.input_queries as input_query

from core.api import APISession, access_next_data_key_decorator, access_next_data_key
from origin_sdk.types.error_types import ProjectProductNotFound
from origin_sdk.types.project_types import InputProject, ProjectSummaryType, ProjectType
from origin_sdk.types.scenario_types import (
    InputScenario,
    ScenarioSummaryType,
    ScenarioType,
)
from origin_sdk.types.input_types import (
    InputsDemand,
    InputsDemandFilter,
    InputsSession,
    TechnologyNames,
    Transform,
)

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
AURORA_ORIGIN_INPUTS_PRODUCTION_ENDPOINT = "https://api.auroraer.com/modelInputs"
AURORA_ORIGIN_INPUTS_STAGE_ENDPOINT = "https://api-staging.auroraer.com/modelInputs"

STAGING = "staging"
PRODUCTION = "production"

ENDPOINTS = {
    STAGING: {
        "scenario": AURORA_ORIGIN_SCENARIO_STAGE_ENDPOINT,
        "inputs": AURORA_ORIGIN_INPUTS_STAGE_ENDPOINT,
    },
    PRODUCTION: {
        "scenario": AURORA_ORIGIN_SCENARIO_PRODUCTION_ENDPOINT,
        "inputs": AURORA_ORIGIN_INPUTS_PRODUCTION_ENDPOINT,
    },
}


def get_endpoints(universe: str = PRODUCTION) -> Dict[str, str]:
    return ENDPOINTS.get(universe, ENDPOINTS.get(PRODUCTION))


class OriginSessionConfig(TypedDict, total=False):
    token: str
    universe: str
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
    dash_config_cache: Any = None

    def __init__(self, config: OriginSessionConfig = {}):
        super().__init__(config.get("token"), config.get("universe"))
        self.scenario_service_url = self._get_base_url(
            # It'll default to production endpoints if universe is not set
            default_url=get_endpoints(config.get("universe")).get("scenario"),
            base_url=config.get("scenario_base_url"),
            environment_variable=AURORA_ORIGIN_SCENARIO_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME,
        )
        self.scenario_service_graphql_url = f"{self.scenario_service_url}/v1/graphql"
        self.inputs_service_url = self._get_base_url(
            # It'll default to production endpoints if universe is not set
            default_url=get_endpoints(config.get("universe")).get("inputs"),
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

    def __inputs_gql_request_with_loading_handler(
        self, url: str, query: str, variables: Any
    ):
        data = None
        while data is None:
            try:
                data = self._graphql_request(url, query, variables)
            except Exception as e:
                try:
                    # Get the GQL error array
                    gql_error_array = e.args[0]

                    # Check the data loading perfect conditions
                    only_one_error = len(gql_error_array) == 1
                    error = gql_error_array[0] if only_one_error else {}
                    error_is_not_ready = "DataNotReady" == error.get("errorKey")

                    # If it's only a data loading error, we should feel free to
                    # try again after a short delay
                    if only_one_error and error_is_not_ready:
                        retry_sleep_in_seconds = 2.5
                        message = error.get("message")
                        log.info(
                            dedent(
                                f"""\
                                Data not ready.
                                Will auto retry in
                                {retry_sleep_in_seconds}s.
                                ({message})
                                """
                            ).replace("\n", " ")
                        )
                        sleep(retry_sleep_in_seconds)
                    else:
                        # Not the right conditions. Re-raise the original error
                        # and let downstream handle (or not)
                        raise e
                except Exception:
                    # Our parsing of this error message has resulted in
                    # something we didn't expect. We might not be a GQL error.
                    # Re-throw the original error instead of a red herring
                    # KeyError from this error handling function
                    raise e

        return data

    def __inputs_gql_workbook_status(self, scenario_id: str):
        request_id = None

        while True:
            variables = {
                "sessionId": scenario_id,
                "requestId": request_id,
            }

            # Get the workbook status
            response = self._graphql_request(
                self.inputs_service_graphql_url,
                input_query.get_workbook_status,
                variables,
            )

            workbook_status = response["getWorkbookStatus"]

            if workbook_status["generationStatus"] == "Requested":
                # We will get a request ID back, so we can use that to check
                # the status again.
                log.info("Waiting for workbook generation to complete")
                sleep(2.5)
                request_id = workbook_status["requestId"]
                continue

            elif workbook_status["generationStatus"] == "Completed":
                # We will get a download URL back, so we can use that to
                # download the workbook.
                return workbook_status["downloadURL"]

            else:
                raise Exception(
                    f"""Workbook generation failed for scenario: {scenario_id}.
                        Request ID: {request_id}. Please try again."""
                )

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

    def __get_dash_config(self):
        if self.dash_config_cache is None:
            url = self.scenario_service_graphql_url
            self.dash_config_cache = self._graphql_request(
                url, project_query.get_origin_dash_config
            )

        return self.dash_config_cache

    def get_project_product_id(self, product: Union[str, int]):
        products = self.__get_dash_config().get("products")
        product_matches = [
            p for p in products if product in [p.get("productId"), p.get("name")]
        ]
        try:
            return product_matches[0].get("productId")
        except IndexError:
            raise ProjectProductNotFound(
                f"""Could not use product {product}. Accepted products are any
                 name or id in: \n{dumps(products, indent=4)}"""
            )

    def create_project(self, project: InputProject) -> ProjectSummaryType:
        """"""
        url = f"{self.scenario_service_graphql_url}"
        if "productId" in project:
            project["productId"] = self.get_project_product_id(project["productId"])

        variables = {"project": project}
        return self._graphql_request(url, project_query.create_project, variables)

    def update_project(self, project_update) -> ProjectSummaryType:
        """ """
        url = f"{self.scenario_service_graphql_url}"
        if "productId" in project_update:
            project_update["productId"] = self.get_project_product_id(
                project_update["productId"]
            )

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

    def get_inputs_session(self, scenario_id: str) -> InputsSession:
        """Gets the inputs instance information, as well as rehydrating all the
        data if required"""
        url = f"{self.inputs_service_graphql_url}"
        variables = {"sessionId": scenario_id}
        return self._graphql_request(
            url, input_query.get_session_information_gql, variables
        )

    def get_model_files(self, scenario_id: str) -> Dict[str, Any]:
        """
        Lists the model files for a scenario, for all runs and years.
        Each file is represented by a file URL, which maybe used to generate
        downloadable URLs later. Please note that the files will not be available
        after the retention period has expired.

        This feature is for internal use only.

        Args:
           scenario_id (string) - The Scenario ID of the scenario to get model files for.
        """

        # Retrieve scenario information once and handle the absence of 'runDetails' early.
        scenario = self.get_scenario_by_id(scenario_id)
        run_details = scenario.get("runDetails")
        if run_details is None:
            raise ValueError(
                f"Scenario {scenario_id} has no run details. Please run the scenario first."
            )

        model_files = {}

        # Build all URLs before making requests.
        urls = []
        for i, run in enumerate(run_details):
            base_url = f"{self.scenario_service_url}/v1/modelFiles/{scenario_id}?runGlobalId={run['runGlobalId']}"
            run_type = run.get("runType", "UnknownRunType_" + str(i))
            years = run.get("years")

            if years:
                # Non Sample Year Runs have a list of years
                model_files[run_type] = {}
                for year in years:
                    year_str = str(year.get("year"))
                    year_full_data_url = f"{base_url}&year={year_str}"
                    urls.append((year_full_data_url, run_type, year_str))
            else:
                urls.append((base_url, run_type, None))

        # Make all HTTP requests and handle responses.
        # The url_for_requesting_model_files is the complete
        # url for requesting model files for a given run type and year.
        # The response is a json object containing the model files for
        # the given run type and year.
        for url_for_requesting_model_files, run_type, year_str in urls:
            response = self.session.request("GET", url_for_requesting_model_files)
            if response.status_code == 200:
                if year_str:
                    model_files[run_type][year_str] = response.json()
                else:
                    model_files[run_type] = response.json()
            else:
                log.info(
                    f"""Failed to get model files for run type {run_type} and year {year_str}.
                    Status: {response.status_code}."""
                )

        return model_files

    def get_model_file_download_url(self, file_url: str) -> str:
        """
        Gets the model file downloadable URL for a given model file url.
        This feature is for internal use only.

        Args:
            file_url (string) - The model file URL to get the download URL for
        """

        base_url = f"{self.scenario_service_url}"
        full_data_url = f"{base_url}/{file_url}"

        response = self.session.request("GET", full_data_url)

        if response.status_code != 200:
            raise ValueError(
                f"Failed to get model file download URL. Status: {response.status_code}. Please check the File URL."
            )

        return response.url

    def __get_inputs_config(self):
        if self.inputs_config_cache is None:
            url = self.inputs_service_graphql_url
            self.inputs_config_cache = self._graphql_request(
                url, input_query.get_config_gql
            )
        return self.inputs_config_cache

    @access_next_data_key_decorator
    def get_technology_names(self, scenario_id: str) -> TechnologyNames:
        """Gets the technology names available for update, by region, and any
        subtechnology groupings"""
        url = f"{self.inputs_service_graphql_url}"
        variables = {"sessionId": scenario_id}
        return self.__inputs_gql_request_with_loading_handler(
            url, input_query.get_technology_names_gql, variables
        )

    @access_next_data_key_decorator
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
        """Gets a specific technology information and all it's yearly and non
        yearly values available for update"""
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
        config = self.__get_inputs_config().get("technology")
        return self.__inputs_gql_request_with_loading_handler(
            url, input_query.get_technology_gql(config), variables
        )

    @access_next_data_key_decorator
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
        """Updates an endogenous technology assumption."""
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

        config = self.__get_inputs_config().get("technology")

        return self._graphql_request(
            url, input_query.update_endo_technology_gql(config), variables
        )

    @access_next_data_key_decorator
    def update_technology_exogenous(
        self,
        scenario_id: str,
        technology_name: str,
        parameter: str,
        transform: List[Transform],
        region: str,
        sub_region: Optional[str] = None,
        subsidy: Optional[str] = None,
        sub_technology: Optional[str] = None,
    ):
        """Updates an exogenous technology assumption."""
        url = f"{self.inputs_service_graphql_url}"
        variables = {
            "sessionId": scenario_id,
            "parameter": parameter,
            "tx": transform,
            "name": technology_name,
            "region": region,
            "subRegion": sub_region,
            "subsidy": subsidy,
            "subTechnology": sub_technology,
        }

        config = self.__get_inputs_config().get("technology")

        return self._graphql_request(
            url, input_query.update_exo_technology_gql(config), variables
        )

    def get_demand_regions(self, scenario_id: str) -> List[str]:
        """Gets the regions of demand available for the current scenario"""
        url = f"{self.inputs_service_graphql_url}"
        variables = {
            "sessionId": scenario_id,
        }

        # getSession will be accessed by default
        response = self.__inputs_gql_request_with_loading_handler(
            url, input_query.get_demand_regions_gql, variables
        )

        # This will dive into the getDemand object
        demand_array = access_next_data_key(response)

        # This will be an array of objects with a "region" field
        return [demand.get("region") for demand in demand_array]

    @access_next_data_key_decorator
    def get_demand(
        self,
        scenario_id: str,
        demand_filter: Optional[InputsDemandFilter] = None,
        aggregate_regions=False,
    ) -> List[InputsDemand]:
        """Gets system demand and demand technology assumptions for this scenario"""
        url = f"{self.inputs_service_graphql_url}"
        variables = {
            "sessionId": scenario_id,
            "demandFilter": demand_filter,
            "aggregateRegions": aggregate_regions,
        }

        config = self.__get_inputs_config().get("demand")

        return self.__inputs_gql_request_with_loading_handler(
            url, input_query.get_demand_gql(config), variables
        )

    @access_next_data_key_decorator
    def update_system_demand(
        self,
        scenario_id: str,
        region: Union[str, List[str]],
        variable: str,
        transform: List[Transform],
        auto_capacity_market_target: Optional[bool] = None,
    ):
        """Updates a system demand parameter for one or more regions. (A system
        demand parameter is one that appears under variables of the main demand
        object, and not one of the demand technologies variables)."""
        url = f"{self.inputs_service_graphql_url}"
        variables = {
            "sessionId": scenario_id,
            "regions": [region] if type(region) is str else region,
            "variable": variable,
            "autoCapacityMarketTarget": auto_capacity_market_target,
            "tx": transform,
        }

        config = self.__get_inputs_config().get("demand")

        return self.__inputs_gql_request_with_loading_handler(
            url, input_query.update_system_demand_gql(config), variables
        )

    @access_next_data_key_decorator
    def get_demand_technology_names(
        self, scenario_id: str, demand_technology_filter: Optional[Any] = None
    ) -> List[InputsDemand]:
        """Gets just demand technology names available, as well as the regions
        they each belong to."""
        url = f"{self.inputs_service_graphql_url}"
        variables = {
            "sessionId": scenario_id,
            "demTechFilter": demand_technology_filter,
        }

        return self.__inputs_gql_request_with_loading_handler(
            url, input_query.get_demand_technology_names, variables
        )

    @access_next_data_key_decorator
    def get_demand_technologies(
        self, scenario_id: str, demand_technology_filter: Optional[Any] = None
    ) -> List[InputsDemand]:
        """Gets just demand technologies, without system demand information."""
        url = f"{self.inputs_service_graphql_url}"
        variables = {
            "sessionId": scenario_id,
            "demTechFilter": demand_technology_filter,
        }

        config = self.__get_inputs_config().get("demand")

        return self.__inputs_gql_request_with_loading_handler(
            url, input_query.get_demand_technologies_gql(config), variables
        )

    @access_next_data_key_decorator
    def update_demand_technology_variable(
        self,
        scenario_id: str,
        region: Union[str, List[str]],
        technology: str,
        variable: str,
        transform: List[Transform],
        auto_capacity_market_target: Optional[bool] = None,
    ) -> List[InputsDemand]:
        """Updates a demand technology variable for one or more regions. (A
        demand technology variable is one that appears on a demand technology
        object, rather than on the system level demand object)."""

        url = f"{self.inputs_service_graphql_url}"
        variables = {
            "sessionId": scenario_id,
            "regions": [region] if type(region) is str else region,
            "variable": variable,
            "technology": technology,
            "autoCapacityMarketTarget": auto_capacity_market_target,
            "tx": transform,
        }

        config = self.__get_inputs_config().get("demand")

        return self.__inputs_gql_request_with_loading_handler(
            url, input_query.update_demand_technology(config), variables
        )

    @access_next_data_key_decorator
    def get_commodities(
        self,
        scenario_id: str,
        native_units_flag: Optional[bool] = None,
        regions: Optional[List[str]] = None,
        commodities: Optional[List[str]] = None,
    ):
        """Gets commodities data.

        Arguments:
            scenario_id (String): ID of the scenario to get the commodities data from
            native_units_flag (Optional, Boolean): What units should be used
            on the return data, MWh or the "native units" the commodities
            come in. Defaults to false.
            regions (Optional, List[String]): If given, will filter the
            commodity prices to the region specifically. By default, we will
            perform an equally weighted global average.
            commodities (Optional, List[String]): If given, will filter the
            commodities to the ones specified. By default, we will
            query for all commodities.
        """
        url = self.inputs_service_graphql_url

        variables = {
            k: v
            for k, v in {
                "sessionId": scenario_id,
                "regions": regions,
                "nativeUnitsFlag": native_units_flag,
                "commodities": commodities,
            }.items()
            if v is not None
        }

        return self.__inputs_gql_request_with_loading_handler(
            url, input_query.get_commodities_gql, variables
        )

    @access_next_data_key_decorator
    def update_commodity_price(
        self,
        scenario_id: str,
        commodity: str,
        regions: List[str],
        transform: List[Transform],
        native_units_flag: Optional[bool] = None,
    ):
        """Updates a commodity price.

        Arguments:
            scenario_id (String): ID of the scenario to get the commodities data from
            come in. Defaults to false.
            commodity (String): The commodity to update.
            regions (List[String]): The regions to update. You can use the
            regions array on the "get commodities" return object to inform the
            view you should update.
            transform (List[Transform]): The transform array used in all updates
            native_units_flag (Optional, Boolean): What units should be used
            on the return data, MWh or the "native units" the commodities

        """
        url = self.inputs_service_graphql_url
        variables = {
            k: v
            for k, v in {
                "sessionId": scenario_id,
                "commodity": commodity,
                "regions": regions,
                "tx": transform,
                "nativeUnitsFlag": native_units_flag,
            }.items()
            if v is not None
        }

        return self.__inputs_gql_request_with_loading_handler(
            url, input_query.update_commodity_gql, variables
        )

    @access_next_data_key_decorator
    def change_base_commodities_assumptions(
        self, scenario_id: str, rebase_reference_id: str
    ):
        """Function to change the underlying commodities assumptions. This
        changes the *original* values, and then any changes you have made (e.g.
        +15%) will apply over the top."""

        url = self.inputs_service_graphql_url
        variables = {
            k: v
            for k, v in {
                "sessionId": scenario_id,
                "rebaseReferenceId": rebase_reference_id,
            }.items()
            if v is not None
        }

        return self.__inputs_gql_request_with_loading_handler(
            url, input_query.rebase_commodities_gql, variables
        )

    @access_next_data_key_decorator
    def get_interconnectors_connections(self, scenario_id: str) -> Dict[str, List[str]]:
        """Gets a dictionary of interconnector connections between regions for
        the given scenario.

        Arguments:
            scenario_id (String): ID of the scenario to get the interconnector data from
        """

        variables = {
            "sessionId": scenario_id,
        }

        interconnector_ends = self.__inputs_gql_request_with_loading_handler(
            self.inputs_service_graphql_url,
            input_query.get_interconnectors_regions_gql(),
            variables,
        )

        all_connections = list(
            map(lambda x: x["ends"], interconnector_ends["getInterconnectors"])
        )

        # Initialize a dictionary with default value of set to store connections
        connection_dict = defaultdict(set)

        # For each pair in all connections, add the pair to the dictionary. Since
        # the dictionary has a default value of set, the set will be created if
        # it doesn't exist, and the pair will be added to the set.
        for pair in all_connections:
            connection_dict[pair[0]].add(pair[1])
            connection_dict[pair[1]].add(pair[0])

        # Convert the sets in the dictionary to lists and return the dictionary
        return {k: list(v) for k, v in connection_dict.items()}

    @access_next_data_key_decorator
    def get_interconnectors(
        self, scenario_id: str, region: str, connection_region: str
    ):
        """Gets the interconnector data between two regions.

        Arguments:
            scenario_id (String): ID of the scenario to get the interconnector data from
            region (String): The region the interconnector is to/from
            connection_region (String): The connected region the interconnector is from/to
        """

        variables = {
            "interconnectorFilter": {
                "OR": [
                    {
                        "from": region,
                        "to": connection_region,
                    },
                    {
                        "from": connection_region,
                        "to": region,
                    },
                ]
            },
            "sessionId": scenario_id,
        }

        config = self.__get_inputs_config().get("interconnectors")

        return self.__inputs_gql_request_with_loading_handler(
            self.inputs_service_graphql_url,
            input_query.get_interconnectors_gql(config),
            variables,
        )

    @access_next_data_key_decorator
    def update_interconnectors(
        self,
        scenario_id: str,
        from_region: str,
        to_region: str,
        variable: str,
        transform: List[Transform],
    ):
        """Function to update a interconnector variable between two regions.

        Arguments:
            scenario_id (String): ID of the scenario to update the interconnector data from
            from_region (String): The region the interconnector is from
            to_region (String): The region the interconnector is to
            variable (String): The variable to update
            transform (List[Transform]): The transform array used in all updates
        """

        variables = {
            "sessionId": scenario_id,
            "from": from_region,
            "to": to_region,
            "variable": variable,
            "tx": transform,
        }

        config = self.__get_inputs_config().get("interconnectors")

        return self.__inputs_gql_request_with_loading_handler(
            self.inputs_service_graphql_url,
            input_query.update_interconnectors(config),
            variables,
        )

    @access_next_data_key_decorator
    def get_workbook_download_url(self, scenario_id: str):
        """
        Will request the generation of an inputs workbook and then return
        a URL to download the workbook from once it's ready.

        Arguments:
            scenario_id (String): ID of the scenario to get the workbook download URL from
        """

        return self.__inputs_gql_workbook_status(scenario_id)

    def get_weather_year_list(self, scenario_id: str):
        """
        Provides list of weather years that are supported for this scenario.
        Returns empty list if weather year feature not supported.

        Arguments:
            scenario_id (String): ID of the scenario for which to check for supported weather years
        """

        variables = {"scenarioGlobalId": scenario_id}

        return self._graphql_request(
            self.scenario_service_graphql_url,
            scenario_query.get_weather_years,
            variables,
        )["years"]

    @lru_cache
    def _get_regions(self):
        return self._graphql_request(
            self.scenario_service_graphql_url, project_query.get_origin_regions
        )
