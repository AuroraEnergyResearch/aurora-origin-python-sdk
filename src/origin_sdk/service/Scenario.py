import logging
from origin_sdk.OriginSession import OriginSession
from typing import Optional
from tempfile import TemporaryDirectory
import pandas as pd
from io import StringIO

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

    def get_scenario_regions(self):
        """
        Helper function to get the regions object on the Scenario, as it's a
        common access pattern.
        """
        return self.scenario.get("regions")

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

        meta = self.get_scenario_region(region)

        # We might have cached the meta_json for this region before
        if "__meta_json" not in meta:
            # If not, get the meta json from the service
            meta_json = self.session.get_meta_json(meta.get("metaUrl"))

            # Store the meta json into state for easier usage later
            meta["__meta_json"] = meta_json

        return meta.get("__meta_json")

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
    ):
        """
        Downloads a csv from the service and returns as a string. Recommended to
        use if looking to generate a csv file on disk.

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
            CSV as text string

        """

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
        base_url = self.get_scenario_region(region).get("dataUrlBase")

        # Decide which currency to use, falling back to the defaultCurrency
        download_currency = currency or self.scenario.get("defaultCurrency")

        # Use a replace to make sure the right currency is used
        filename: str = download_meta.get("filename").replace(
            "{currency}", download_currency
        )

        # Request the data url. Use noredirect in order to make the re-request
        # to s3 ourselves.
        full_data_url = (
            f"{self.session.scenario_service_url}/{base_url}{filename}?noredirect=true"
        )
        logger.debug(full_data_url)

        # Make the request for the timed URL
        s3_request = self.session.session.request("GET", full_data_url)

        # Get the location of the redirect
        s3_location = s3_request.headers.get("location")

        # Make a follow up request for the data
        return self.session.session.request("GET", s3_location).text

    def get_scenario_dataframe(
        self,
        region: str,
        download_type: str,
        granularity: str,
        currency: Optional[str] = None,
    ):
        """
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
        data = self.get_scenario_data_csv(
            region=region,
            download_type=download_type,
            granularity=granularity,
            currency=currency,
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
