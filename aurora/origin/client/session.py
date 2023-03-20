from json import encoder
from aurora.amun.client.responses import (
    RegionDetail,
    get_RegionDetail_from_response,
)
from aurora.amun.client.parameters import (
    FlowParameters,
    LoadFactorBaseParameters,
)
from typing import Dict, List
import requests
import logging
import os
from pathlib import Path
import json
from urllib.parse import urlencode
from aurora.amun.client.utils import AmunJSONEncoder, configure_session_retry


log = logging.getLogger(__name__)
AURORA_API_KEY_ENVIRONMENT_VARIABLE_NAME = "AURORA_API_KEY"
AURORA_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME = "AURORA_API_BASE_URL"
AURORA_API_KEY_FILE_NAME = ".aurora-api-key"
AURORA_ORIGIN_PRODUCTION_ENDPOINT = "https://api.auroraer.com/scenExplr/v1"
AURORA_ORIGIN_STAGE_ENDPOINT = "https://api-staging.auroraer.com/scenExplr/v1"


class APISession:
    """Internal class to hold base methods for interacting with the Aurora HTTP API"""

    def __init__(self, base_url=None, token=None):
        self.token = self._get_token(token)
        self.base_url = self._get_base_url(base_url)
        self.session = self._create_session()

    def _get_token(self, token, universe=None):
        env_key = f"{AURORA_API_KEY_ENVIRONMENT_VARIABLE_NAME}"
        if universe is not None:
            env_key = f"{AURORA_API_KEY_ENVIRONMENT_VARIABLE_NAME}_{universe}"

        if token is not None:
            log.debug(f"Using token passed as parameter to session constructor")
            return token
        elif env_key in os.environ:
            log.debug(f"Using token passed found in environment variable {env_key}")
            return os.environ[env_key]
        else:
            return self._load_token_from_file(universe)

    def _get_base_url(self, base_url):
        if base_url is not None:
            log.debug(
                f"Using baseUrl {base_url} passed as parameter to session constructor"
            )
            return base_url
        elif AURORA_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME in os.environ:
            base_url_override = os.environ[
                AURORA_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME
            ]
            log.debug(
                f"Using base url '{base_url_override}' passed found in environment variable {AURORA_API_BASE_URL_ENVIRONMENT_VARIABLE_NAME}"
            )
            return base_url_override
        else:
            return AURORA_CHRONOS_PRODUCTION_ENDPOINT

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
                f"No aurora api key file found '{file}'. Please create the text file '{AURORA_API_KEY_FILE_NAME}' file in your home directory {Path.home()} and add you api token to it."
            )

    def _create_session(self):
        log.info(f"Creating session with token '**************{self.token[-5:]}'")
        session = session = requests.session()
        session.headers = {
            "Content-Type": "application/json",
            "Private-Token": self.token,
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
                f"You are not authorised. Please check you have set the correct api token."
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

    def _parse_as_json(self, response):
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise RuntimeError(
                f"You are not authorised. Please check you have set the correct api token. (*******{self.token[-5:]})"
            )
        elif response.status_code == 403:
            raise RuntimeError(
                f"Your token is valid but you do not have the required permissions to perform this operation.(*******{self.token[-5:]})"
            )
        else:
            raise RuntimeError(f"{response.status_code}  {response.text}")


class OriginSession(APISession):
    """Manage access to the Origin API.

    By default the session will connect to the production Origin API endpoint. This can be overridden by passing the base_url into the constructor
    or by setting the environment variable *AURORA_API_BASE_URL*. This feature is for internal use only.

    The authentication token is read from the users home directory *$home/.aurora-api-key* e.g. *C:/Users/Joe Bloggs/.aurora-api-key*.
    This can be overridden by passing the token into the constructor or by setting the environment variable *AURORA_API_KEY*.

    Args:
        base_url (string, optional): Override the base url used to contact the Origin API. Defaults to None.
        token (string, optional): Overide the api authentication token used for API access. Defaults to None.
    """

    def __init__(self, base_url=None, token=None):
        super().__init__(base_url, token)
