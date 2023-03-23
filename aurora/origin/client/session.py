from json import encoder

from typing import Dict, List, Optional
import requests
import logging
import os
from pathlib import Path
import json
from urllib.parse import urlencode
import aurora.origin.client.gql.queries.project as project_query
import aurora.origin.client.gql.queries.scenario as scenario_query

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

AURORA_API_KEY_ENVIRONMENT_VARIABLE_NAME = "AURORA_API_KEY"
AURORA_ORIGIN_SCENARIO_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME = (
    "AURORA_ORIGIN_SCENARIO_API_BASE_URL"
)
AURORA_ORIGIN_INPUTS_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME = (
    "AURORA_ORIGIN_INPUTS_API_BASE_URL"
)
AURORA_API_KEY_FILE_NAME = ".aurora-api-key"
AURORA_ORIGIN_SCENARIO_PRODUCTION_ENDPOINT = "https://api.auroraer.com/scenarioExplr"
AURORA_ORIGIN_SCENARIO_STAGE_ENDPOINT = "https://api-staging.auroraer.com/scenarioExplr"
AURORA_ORIGIN_INPUTS_PRODUCTION_ENDPOINT = "https://app.auroraer.com/modelInputs"
AURORA_ORIGIN_INPUTS_STAGE_ENDPOINT = "https://app-staging.auroraer.com/modelInputs"


class APISession:
    """Internal class to hold base methods for interacting with the Aurora HTTP API"""

    def __init__(self, token=None):
        self.token = self._get_token(token)
        self.session = self._create_session()

    def _get_token(self, token, universe=None):
        env_key = f"{AURORA_API_KEY_ENVIRONMENT_VARIABLE_NAME}"
        if universe is not None:
            env_key = f"{AURORA_API_KEY_ENVIRONMENT_VARIABLE_NAME}_{universe}"

        if token is not None:
            log.debug("Using token passed as parameter to session constructor")
            return token
        elif env_key in os.environ:
            log.debug(f"Using token passed found in environment variable {env_key}")
            return os.environ[env_key]
        else:
            return self._load_token_from_file(universe)

    def _get_base_url(
        self,
        default_url: str,
        base_url: Optional[str] = None,
        environment_variable: Optional[str] = None,
    ):
        if base_url is not None:
            log.debug(
                f"Using baseUrl {base_url} passed as parameter to session constructor"
            )
            return base_url
        elif environment_variable in os.environ:
            base_url_override = os.environ[environment_variable]
            log.debug(
                f"""Using base url '{base_url_override}' passed found in
                 environment variable
                 {environment_variable}"""
            )
            return base_url_override
        else:
            return default_url

    def _load_token_from_file(self, universe):
        file = Path.joinpath(Path.home(), AURORA_API_KEY_FILE_NAME)
        if universe is not None:
            file = Path.joinpath(Path.home(), f"{AURORA_API_KEY_FILE_NAME}.{universe}")

        log.debug(f"Looking for token in '{file}'")
        key_found = []
        if Path.exists(file):
            with open(file, "r") as reader:
                key_found = reader.readlines()
            if len(key_found) == 1:
                return key_found[0]
            else:
                raise RuntimeError(f"Could not parse key from file {file}")
        else:
            raise RuntimeError(
                f"""No aurora api key file found '{file}'. Please create the
                 text file '{AURORA_API_KEY_FILE_NAME}' file in your home
                 directory {Path.home()} and add you api token to it."""
            )

    def _create_session(self):
        log.info(f"Creating session with token '**************{self.token[-5:]}'")
        session = session = requests.session()
        session.headers = {
            "Content-Type": "application/json",
            "Private-Token": self.token,
            "EOS-Cookie": self.token,
        }
        return session

    def _get_request(self, url, params={}):
        log.debug(f"GET Request to {url}  with params {params}")

        response = self.session.request("GET", url, params=params)
        return self._parse_as_json(response)

    def _del_request(self, url, params={}):
        log.debug(f"DEL Request to {url}  with params {params}")

        response = self.session.request("DELETE", url, params=params)
        if response.status_code == 200:
            return
        elif response.status_code == 401:
            raise RuntimeError(
                "You are not authorised. Please check you have set the correct api token."
            )
        else:
            raise RuntimeError(f"{response.status_code}  {response.text}")

    def _put_request(self, url, payload):
        log.debug(f"PUT Request to {url} with payload {payload}")
        response = self.session.request("PUT", url, data=json.dumps(payload))
        return self._parse_as_json(response)

    def _post_request(self, url, payload):
        log.debug(f"POST Request to {url} with payload {payload}")
        response = self.session.request("POST", url, data=json.dumps(payload))
        return self._parse_as_json(response)

    def _graphql_request(self, url, query, variables):
        return self._post_request(url, {"query": query, "variables": variables})

    def _parse_as_json(self, response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise RuntimeError(
                f"""You are not authorised. Please check you have set the
                 correct api token. (*******{self.token[-5:]})"""
            )
        elif response.status_code == 403:
            raise RuntimeError(
                f"""Your token is valid but you do not have the required
                 permissions to perform this
                 operation.(*******{self.token[-5:]})"""
            )
        else:
            raise RuntimeError(f"{response.status_code}  {response.text}")


class OriginSession(APISession):
    """Manage access to the Origin API.

    By default the session will connect to the production Origin API endpoint.
    This can be overridden by passing the base_url into the constructor or by
    setting the environment variable *AURORA_API_BASE_URL*. This feature is for
    internal use only.

    The authentication token is read from the users home directory
    *$home/.aurora-api-key* e.g. *C:/Users/Joe Bloggs/.aurora-api-key*. This can
    be overridden by passing the token into the constructor or by setting the
    environment variable *AURORA_API_KEY*.

    Args:
        token (string, optional): Override the api authentication token used for
        API access. Defaults to None.
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
        variables = {"filter": {"scenarioGlobalId": id}}
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
