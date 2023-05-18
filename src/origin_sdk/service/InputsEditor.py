import logging
from typing import Optional
from origin_sdk.OriginSession import OriginSession
from origin_sdk.types.input_types import InputsSession, TechnologyNames


logger = logging.getLogger(__name__)


class InputsEditor:
    """
    -- BETA --

    Not suitable for wide consumption yet, preliminary user-friendly wrapper around
    the Inputs Service API calls.

    WARNING: If using, the contract defined here is subject to change.
    """

    def __init__(self, scenario_id: str, session: OriginSession):
        self.scenario_id = scenario_id
        self.session = session
        self.inputs_session: InputsSession = session.get_inputs_session(scenario_id)
        self.technology_names: TechnologyNames = None

    def get_demand_regions(self):
        """Gets the regios available for get/update demand functionality in
        A Origin. Regional availability is affected by the "main region" the scenario has been
        configured to run."""
        return self.session.get_demand_regions(self.scenario_id)

    def get_demand_for_region(self, region: str):
        return self.session.get_demand(
            self.scenario_id, {"region": region} if region else None
        )[0]

    def get_technology_names(self) -> TechnologyNames:
        """
        Gets the technology names available for use in get/update technology
        functionality in Origin.

        Caches into the state of the instance for ease of use.

        Returns:
            TechnologyNames object (see types.input_types for details) General
            structure is as follows: {
                [region]: {
                    [technologyName]: {
                        subTechnologiesExogenous: List[str],
                        subTechnologiesEndogenous: List[str], subRegions: {
                            [subregion]: {
                                subsidies: List[str] subTechnologiesExogenous:
                                List[str], subTechnologiesEndogenous: List[str],
                            }
                        }
                    }
                }
            }
        """
        if self.technology_names is None:
            self.technology_names = self.session.get_technology_names(self.scenario_id)

        return self.technology_names
