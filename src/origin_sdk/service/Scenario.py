import logging
import pandas as pd

from origin_sdk.OriginSession import OriginSession
from core.data import (
    get_meta_json_from_cache,
    save_meta_json_to_cache,
    get_scenario_outputs_from_cache,
    save_scenario_outputs_to_cache,
)
from typing import List, Optional, Union, cast
from io import StringIO
from datetime import datetime
from time import sleep

from origin_sdk.types.scenario_types import RegionDict

logger = logging.getLogger(__name__)


class Scenario:
    """
    A Scenario class that holds state in order to provide a more Pythonic
    interface for Scenario building and downloading outputs

    Arguments:
        scenario_id (str): The ID to initialise the scenario with. Will fetch
        the scenario details and populate itself with details
        session (OriginSession): You should first instantiate an OriginSession
        and pass this over to the Scenario.

    Attributes:
        scenario_id (str): The scenario ID
        session (OriginSession): The OriginSession attached to this scenario
        scenario (ScenarioType): The full Scenario object from the service
    """

    def __init__(self, scenario_id: str, session: OriginSession):
        self.scenario_id = scenario_id
        self.session = session
        self.scenario = self.session.get_scenario_by_id(scenario_id)

    def get_downloadable_regions(self):
        """
        A helper function to return the regions available for download from
        this scenario

        Returns:
            A list of regions available
        """
        return [region for region in self.scenario.get("regions")]

    def __get_additional_scenario_regions(
        self,
        base_region: str,
        base_region_meta: RegionDict | None,
        base_scenario_regions: dict[str, RegionDict],
    ) -> dict[str, RegionDict]:
        """Get additional regions for a scenario based on region groups."""

        if not base_region_meta:
            return {}

        # Find the region group containing base_region
        regions_data = next(iter(self.session._get_regions().values())).values()
        region_group = next(
            (x for x in regions_data if base_region in x["regions"]), {}
        )

        # Get region codes not already in base_scenario_regions
        all_region_codes = region_group.get("regions", {}).keys()
        additional_codes = [
            code for code in all_region_codes if code not in base_scenario_regions
        ]

        # Construct metadata for each additional region
        def replace_region_in_urls(meta: RegionDict, old: str, new: str) -> RegionDict:
            return {
                "dataUrlBase": meta["dataUrlBase"].replace(f"/{old}/", f"/{new}/"),
                "metaUrl": meta["metaUrl"].replace(f"/{old}/", f"/{new}/"),
                "regionCode": new,
                "__meta_json": None,
            }

        return {
            code: replace_region_in_urls(base_region_meta, base_region, code)
            for code in additional_codes
        }

    def get_scenario_regions(self):
        """
        Helper function to get the regions object on the Scenario, as it's a
        common access pattern.
        """
        scenario_regions = self.scenario.get("regions")

        if not scenario_regions:
            return cast(dict[str, RegionDict], {})

        scenario_region = next(iter(scenario_regions))
        scenario_region_meta = scenario_regions.get(scenario_region)

        additional_regions = self.__get_additional_scenario_regions(
            scenario_region, scenario_region_meta, scenario_regions
        )

        return {**scenario_regions, **additional_regions}

    def get_scenario_region(self, region: str):
        """
        Helper function to get a specific region from the regions object, as
        it's a common access pattern.

        Returns:
            RegionDict
        """
        return self.get_scenario_regions().get(region)

    def __get_download_meta_for_region(self, region: str):
        """
        A helper function that gets the meta json for the region. Caches into
        internal state for future use. Required to see what downloads are
        available (see `get_download_types`) or for constructing the download
        URL (See `get_scenario_data_csv` and `get_scenario_dataframe`).

        This function is not likely to be useful outside of internal
        implementation.

        Returns:
            meta_json object, defining the downloads available and what they contain.
        """
        from_cache = get_meta_json_from_cache(self.scenario_id, region)
        if from_cache is not None:
            return from_cache

        meta = self.get_scenario_region(region)
        if not meta:
            raise Exception(
                f"Region '{region}' not found for scenario with ID '{self.scenario_id}'"
            )

        meta_json = self.session.get_meta_json(meta.get("metaUrl"))

        save_meta_json_to_cache(self.scenario_id, region, meta_json)

        return meta_json

    def get_download_types(self, region: str):
        """
        Returns the types and granularities of download available for the region. Expect something
        like "system"|"technology" and "1y"|"1m" for type and granularity
        respectively.

        Arguments:

            region (String)

        Returns:
            A list of type and granularity downloads available for the region.
        """

        meta_json = self.__get_download_meta_for_region(region)

        return [
            {
                "type": definition.get("type"),
                "granularity": definition.get("granularity"),
            }
            for definition in meta_json["dataDefinitions"]
        ]

    def get_scenario_data_csv(
        self,
        region: str,
        download_type: str,
        granularity: str,
        currency: Optional[str] = None,
        node: Optional[str] = None,
        force_no_cache: bool = False,
        params: Optional[dict[str, str]] = None,
    ):
        """
        Downloads a csv from the service and returns as a string. Recommended to
        use if looking to generate a csv file on disk.

        In general, our csvs have two header rows. The first identifies the
        column of data and the second is a unit string or other contextual
        information if relevant. To convert this to a pandas data frame,
        pass the output of this method to pandas' read_csv() method via a buffer.

        Examples:

        ```py
        csv_data = scenario.get_scenario_data_csv('gbr', 'system', '1y')
        buffer = StringIO(csv_data)
        df = pd.read_csv(buffer, header=[0,1])
        ```

        ```py
        csv_data = scenario.get_scenario_data_csv(
            region='erc',
            download_type='nodal',
            granularity='1h',
            currency='usd2024',
            node='ZONDWD_6_B1',
        )
        buffer = StringIO(csv_data)
        df = pd.read_csv(buffer, header=[0,1])
        ```

        Arguments:
            region (String): The region to download for. Use
            "get_downloadable_regions" to see a list of options.
            download_type (String): The "type" of file to download. You can use
            "get_download_types" to query the available options.
            granularity (String): The "granularity" of file to download. You can use
            "get_download_types" to query the available options.
            currency (Optional, String): The currency year to download the file
            in. Will default to `defaultCurrency` on the scenario if available.
            node (Optional, String): The node identifier to download nodal data for.

        Returns:
            CSV as text string

        """
        addon_params = params or {}

        # Decide which currency to use, falling back to the defaultCurrency
        download_currency = currency or self.scenario.get("defaultCurrency")

        from_cache = get_scenario_outputs_from_cache(
            self.scenario_id,
            region,
            download_type,
            granularity,
            download_currency,
            node,
            addon_params,
        )
        if from_cache is not None and not force_no_cache:
            return from_cache

        # First get the download information
        meta_json = self.__get_download_meta_for_region(region)

        # Then filter the data definitions by requested type and granularity
        download_meta_list = [
            d
            for d in meta_json.get("dataDefinitions")
            if d.get("granularity") == granularity and d.get("type") == download_type
        ]

        number_of_downloads = len(download_meta_list)
        if number_of_downloads != 1:
            issue_str = (
                "Could not find download"
                if number_of_downloads == 0
                else "Ambiguous download"
            )
            ex_msg = (
                f"{issue_str} for {download_type}, {granularity} for {region}. "
                f"Expected 1, found {number_of_downloads}. "
                "Use Scenario.get_download_types to see what available "
                "combinations there are for the scenario."
            )
            raise Exception(ex_msg)

        # Now we have asserted there is only one, get this meta info.
        download_meta = download_meta_list[0]

        # Get the base URL of the download
        region_details = self.get_scenario_region(region)

        if not region_details:
            raise Exception(
                f"Region '{region}' not found for scenario with ID '{self.scenario_id}'"
            )

        base_url = region_details.get("dataUrlBase")

        # Validate node parameter against download metadata
        filename_template = download_meta.get("filename", "")
        node_supported = "{nodename}" in filename_template

        if node and not node_supported:
            # User provided node but download doesn't support it
            logger.warning(
                f"Node parameter provided but download with download type {download_type} does not support it."
            )
            raise Exception(
                f"Download type '{download_type}' with granularity "
                f"'{granularity}' does not support node parameter."
            )
        elif node_supported and not node:
            # Download requires node but user didn't provide it
            raise Exception(
                f"Download type '{download_type}' with granularity "
                f"'{granularity}' requires node parameter, but none was provided."
            )

        # Use a replace to make sure the right currency is used
        filename: str = filename_template.replace(
            "{currency}", download_currency
        ).replace("{nodename}", node or "")

        # Request the data url. Use noredirect in order to make the re-request
        # to s3 ourselves.
        full_data_url = f"{self.session.scenario_service_url}/{base_url}{filename}"
        full_params = {"noredirect": "true", "checkstatus": "true", **addon_params}

        logger.debug(full_data_url)

        while True:
            # Make the request for the timed URL
            s3_request = self.session.session.request("GET", full_data_url, full_params)

            # If we get a 425, we need to wait and try again. Another instance may be
            # generating the file.
            if s3_request.status_code == 425:
                logger.debug("Received 425 Too Early, retrying after 15 seconds...")
                sleep(15)
                continue

            # Get the location of the redirect
            s3_location = s3_request.headers.get("location")

            if not s3_location:
                raise Exception(
                    f"Could not get download location for "
                    f"{download_type}, {granularity} for {region}."
                )

            # Make a follow up request for the data
            csv_as_text = self.session.session.request("GET", s3_location).text

            save_scenario_outputs_to_cache(
                self.scenario_id,
                region,
                download_type,
                granularity,
                download_currency,
                node,
                csv_as_text,
                addon_params,
            )

            return csv_as_text

    def get_scenario_dataframe(
        self,
        region: str,
        download_type: str,
        granularity: str,
        currency: Optional[str] = None,
        force_no_cache: bool = False,
        params: Optional[dict[str, str]] = None,
    ):
        """
        This method is deprecated. Use get_scenario_data_csv instead.

        Example:

            csv_data = scenario.get_scenario_data_csv('gbr', 'system', '1y')
            buffer = StringIO(csv_data)
            df = pd.read_csv(buffer, header=[0,1])

        ---


        Much the same as `get_scenario_data` but instead parses the CSV as a
        pandas data frame for easier consumption via a script. In general, our
        CSVs have two header rows. The first identifies the column of data and
        the second is a unit string or other contextual information if relevant.

        Arguments:
            region (String): The region to download for. Use
            "get_downloadable_regions" to see a list of options.
            type (String): The "type" of file to download. You can use
            "get_download_types" to query the available options.
            granularity (String): The "granularity" of file to download. You can use
            "get_download_types" to query the available options.
            currency (Optional, String): The currency year to download the file
            in. Will default to `defaultCurrency` on the scenario if available.

        Returns:
            Pandas Dataframe
        """
        logger.warning(
            "get_scenario_dataframe is deprecated. Use get_scenario_data_csv instead."
        )

        data = self.get_scenario_data_csv(
            region=region,
            download_type=download_type,
            granularity=granularity,
            currency=currency,
            force_no_cache=force_no_cache,
            params=params,
        )
        buffer = StringIO(data)
        df = pd.read_csv(buffer, header=[0, 1])
        return df

    def refresh(self):
        """
        Contacts the service to get an updated view of the scenario. Useful for
        things such as polling on a frequency.
        """
        self.scenario = self.session.get_scenario_by_id(self.scenario_id)
        return self

    def get(self, key: str):
        """
        Shortcut for Scenario.scenario.get()
        """
        return self.scenario.get(key)

    @staticmethod
    def get_latest_scenario_from_region(
        session: OriginSession,
        region: str,
        name_filter: Optional[Union[str, List[str]]] = None,
    ):
        """Given a region (and optional name match) will return the latest
        scenario found."""

        # Get all scenarios from the region
        regional_scenarios = session.get_aurora_scenarios(region)

        # Sort them based on publication date
        regional_scenarios.sort(
            key=lambda scenario: datetime.fromisoformat(
                scenario["publicationDate"].replace("Z", "")
            ).timestamp(),
            reverse=True,
        )
        try:
            if name_filter is None:
                # Just return the latest scenario
                return Scenario(
                    scenario_id=regional_scenarios[0].get("scenarioGlobalId"),
                    session=session,
                )

            else:
                # Handle the singular name_filter into a multiple
                name_filter = [name_filter] if type(name_filter) == str else name_filter

                # Now filter the list of scenarios by the name filter if it exists
                latest = next(
                    (
                        scenario
                        for scenario in regional_scenarios
                        if all(
                            filter.lower() in scenario.get("name").lower()
                            for filter in name_filter
                        )
                    )
                )

                return Scenario(
                    scenario_id=latest.get("scenarioGlobalId"), session=session
                )
        except (StopIteration, IndexError):
            raise Exception(
                f"""Scenario not found for region '{region}' {
                    f'and filter "{name_filter}"' if name_filter is not None else ""
                }"""
            )
