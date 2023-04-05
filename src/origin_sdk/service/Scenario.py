import logging
from origin_sdk.OriginSession import OriginSession
from typing import Optional
from tempfile import TemporaryDirectory

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

    Properties:
        scenario_id (str): The scenario ID
        session (OriginSession): The OriginSession attached to this scenario
        scenario (ScenarioType): The full Scenario object from the service

    Methods:
        get_downloadable_regions()

    """

    def __init__(self, scenario_id: str, session: OriginSession):
        self.scenario_id = scenario_id
        self.session = session
        self.scenario = self.session.get_scenario_by_id(scenario_id)
        self.temp_dir: Optional[TemporaryDirectory] = None

    def __del__(self):
        # Cleanup
        if self.temp_dir:
            self.temp_dir.cleanup()

    def __get_temporary_directory(self):
        # Only create the temp dir if we need one on demand
        if self.temp_dir:
            return self.temp_dir
        else:
            self.temp_dir = TemporaryDirectory()

    def get_downloadable_regions(self):
        """
        A helper function to return the regions available for download from
        this scenario

        Returns:
            A list of regions available
        """
        return [region for region in self.scenario.get("regions")]

    def get_meta_json(self, region: str):
        """
        A helper function that gets the meta json for the region. Caches into
        internal state for future use.

        Returns:
            A meta json useful for downloading files.
        """

        meta = self.scenario.get("regions").get(region)
        if "meta_json" not in meta:
            meta_json = self.session.get_meta_json(meta.get("metaUrl"))

            # Store the meta json into state for easier usage later
            self.scenario.get("regions").get(region)["meta_json"] = meta_json
        else:
            meta_json = meta["meta_json"]

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

        meta_json = self.get_meta_json(region)

        return [
            {
                "type": definition.get("type"),
                "granularity": definition.get("granularity"),
            }
            for definition in meta_json["dataDefinitions"]
        ]

    def download_output_csv(
        self,
        region: str,
        type: str,
        granularity: str,
        currency: str,
        outfile: Optional[str] = None,
    ):
        """
        Downloads a csv from the service. As of writing, returns the CSV
        directly from the function. Do not use this for half hourly data in it's
        current form, it's a bad idea.

        Arguments:
            region (String): The region to download for. Use
            "get_downloadable_regions" to see a list of options.
            type (String): The "type" of file to download. You can use
            "get_download_types" to query the available options.
            granularity (String): The "granularity" of file to download. You can use
            "get_download_types" to query the available options.
            currency (String): The currency year to download the file in.

        Returns:
            CSV as text

        """

        meta_json = self.get_meta_json(region)

        download_meta_list = [
            d
            for d in meta_json.get("dataDefinitions")
            if d.get("granularity") == granularity and d.get("type") == type
        ]

        if len(download_meta_list) == 0:
            raise Exception(
                f"Could not find download for {type}, {granularity} for {region}"
            )

        download_meta = download_meta_list[0]

        base_url = self.scenario.get("regions").get(region).get("dataUrlBase")
        filename: str = download_meta.get("filename").replace("{currency}", currency)
        full_data_url = (
            f"{self.session.scenario_service_url}/{base_url}{filename}?noredirect=true"
        )
        logger.debug(full_data_url)

        s3_request = self.session.session.request("GET", full_data_url)
        print(s3_request.headers.items())
        s3_location = s3_request.headers.get("location")

        return self.session.session.request("GET", s3_location).text

    def refresh(self):
        """"""
        self.scenario = self.session.get_scenario_by_id(self.scenario_id)
        return self
