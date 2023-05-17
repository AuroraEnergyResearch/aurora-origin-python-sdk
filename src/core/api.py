from typing import Optional
import requests
import logging
import os
from pathlib import Path
import json

log = logging.getLogger(__name__)

AURORA_API_KEY_ENVIRONMENT_VARIABLE_NAME = "AURORA_API_KEY"
AURORA_API_KEY_FILE_NAME = ".aurora-api-key"


def handle_graphql_response(func):
    """Decorator that handles graphql responses and error handling"""

    def parse_data_and_errors_from_gql_response(*args, **kwargs):
        result = func(*args, **kwargs)

        if result.get("errors"):
            errors = result.get("errors")
            raise Exception(errors)

        data = None
        if result.get("data"):
            # Data is not null
            data = result.get("data")

            # If there was only one resolver requested, shortcut and give to the
            # user
            data = access_next_data_key(data)

        return data

    return parse_data_and_errors_from_gql_response


def access_next_data_key(data: dict):
    """Helper function to access the first key of a dict if it's the only thing
    in there. Useful for graphql resolver returns."""

    if len(data) == 1 and type(data) == dict:
        nextkey = next(iter(data.keys()))
        data = next(iter(data.values()))
        log.debug(f"diving into {nextkey} object on data object")

    return data


def access_next_data_key_decorator(func):
    """A decorator version of the above function"""

    def access_next_key_after_execution(*args, **kwargs):
        result = func(*args, **kwargs)

        return access_next_data_key(result)

    return access_next_key_after_execution


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
        elif environment_variable and environment_variable in os.environ:
            base_url_override = os.environ.get(environment_variable)
            log.debug(
                f"""Using base url '{base_url_override}' passed found in
                 environment variable
                 {environment_variable}"""
            )
            return base_url_override

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

    @handle_graphql_response
    def _graphql_request(self, url, query, variables=None):
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
