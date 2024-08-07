from json import dump, load
from appdirs import user_data_dir

import logging
from pathlib import Path
from os import makedirs, environ

# Circular imports causing an issue.
# This pattern taken from
# https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Any imports required for typing that might result in circular deps go here
    pass


app_name = "aer-origin-sdk"
app_author = "auroraenergyresearch"

logger = logging.getLogger(__name__)

AURORA_ORIGIN_CACHE_DIRECTORY = "AURORA_ORIGIN_CACHE_DIRECTORY"


def get_data_directory():
    """Lazy create the data directory. All requests for the data directory
    should come through this function"""
    data_directory = Path(
        environ.get(
            AURORA_ORIGIN_CACHE_DIRECTORY,
            user_data_dir(appname=app_name, appauthor=app_author),
        )
    )

    if not data_directory.exists():
        makedirs(data_directory)

    return data_directory


def get_scenario_cache(id: str):
    """Gets the scenario cache folder from the appdata dir"""
    scenario_dir = get_data_directory() / id

    if not scenario_dir.exists():
        makedirs(scenario_dir)

    return scenario_dir


def get_meta_json_filename(region: str):
    """Single entry point for filename string creation for meta json"""
    return f"meta_{region}.json"


def save_meta_json_to_cache(id: str, region: str, meta_json: dict):
    """Takes care of saving the regional meta json to disk"""
    scenario_dir = get_scenario_cache(id)
    with open(scenario_dir / get_meta_json_filename(region), "w") as f:
        dump(meta_json, f)


def get_meta_json_from_cache(id: str, region: str):
    """Gets the meta json from disk if it exists"""
    scenario_dir = get_scenario_cache(id)
    meta_json = scenario_dir / get_meta_json_filename(region)

    if not meta_json.exists():
        return None

    with open(meta_json, "r") as f:
        return load(f)


def get_scenario_output_filename(
    region: str,
    download_type: str,
    granularity: str,
    currency: str,
    params: dict[str, str],
):
    """Single entry point for filename string creation for scenario downloads"""

    filename = f"{region}-{download_type}-{granularity}-{currency}.csv"

    if bool(params) is True:
        params_hash = hash(frozenset(params.items()))
        filename = f"{params_hash}-{filename}"

    return filename


def save_scenario_outputs_to_cache(
    id: str,
    region: str,
    download_type: str,
    granularity: str,
    currency: str,
    csv: str,
    params: dict[str, str],
):
    """Takes care of saving any scenario outputs to the cache"""
    scenario_dir = get_scenario_cache(id)
    filename = get_scenario_output_filename(
        region, download_type, granularity, currency, params
    )
    file = scenario_dir / filename

    with open(file, "w") as f:
        f.write(csv)


def get_scenario_outputs_from_cache(
    id: str,
    region: str,
    download_type: str,
    granularity: str,
    currency: str,
    params: dict[str, str],
):
    """Gets the scenario output from disk if it exists"""
    scenario_dir = get_scenario_cache(id)
    filename = get_scenario_output_filename(
        region, download_type, granularity, currency, params
    )
    file = scenario_dir / filename

    if not file.exists():
        return None

    with open(file, "r") as f:
        return f.read()
