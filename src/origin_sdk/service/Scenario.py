from origin_sdk.OriginSession import OriginSession, OriginSessionConfig
from typing import get_args


class Scenario:
    """"""

    def __init__(self, scenario_id: str, api_options: OriginSessionConfig):
        self.scenario_id = scenario_id
        self.session = OriginSession(**api_options)
        self.scenario = self.session.get_scenario_by_id(scenario_id)

    def __download_output_csv(self, type: str, granularity: str):
        """"""
        pass

    def get_download_options(self):
        """"""
        return [region for region in self.scenario.regions]

    def refresh(self):
        """"""
        self.scenario = self.session.get_scenario_by_id(self.scenario_id)
        return self
