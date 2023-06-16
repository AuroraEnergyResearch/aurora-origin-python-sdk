from functools import partialmethod
import logging
from typing import List, Optional
from origin_sdk.OriginSession import OriginSession
from origin_sdk.types.input_types import InputsSession, TechnologyNames, Transform


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

    def __get_demand_technology_names(self):
        """
        Service doesn't support this atm
        """
        return self.session.get_demand_technology_names(self.scenario_id)

    def get_demand_technologies(self):
        """
        Gets all the demand techs and the data for them
        """
        return self.session.get_demand_technologies(self.scenario_id)

    def update_system_demand_variable(
        self,
        region: str,
        variable: str,
        transform: List[Transform],
        auto_capacity_market_target: Optional[bool] = None,
    ):
        return self.session.update_system_demand(
            scenario_id=self.scenario_id,
            region=region,
            variable=variable,
            transform=transform,
            auto_capacity_market_target=auto_capacity_market_target,
        )

    def update_demand_technology_variable(
        self,
        region: str,
        technology: str,
        variable: str,
        transform: List[Transform],
        auto_capacity_market_target: Optional[bool] = None,
    ):
        return self.session.update_demand_technology_variable(
            scenario_id=self.scenario_id,
            region=region,
            technology=technology,
            variable=variable,
            transform=transform,
            auto_capacity_market_target=auto_capacity_market_target,
        )

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

    def get_supply_technology(
        self,
        technology_name: str,
        region: str,
        subregion: Optional[str] = None,
        exogenous_sub_technology: Optional[str] = None,
        subsidy: Optional[str] = None,
        endogenous_sub_technology: Optional[str] = None,
    ):
        return self.session.get_technology(
            scenario_id=self.scenario_id,
            technology_name=technology_name,
            region=region,
            subregion=subregion,
            exogenous_sub_technology=exogenous_sub_technology,
            subsidy=subsidy,
            endogenous_sub_technology=endogenous_sub_technology,
        )

    def update_exogenous_technology_variable(
        self,
        technology_name: str,
        parameter: str,
        transform: List[Transform],
        region: str,
        sub_region: Optional[str] = None,
        subsidy: Optional[str] = None,
        sub_technology: Optional[str] = None,
    ):
        return self.session.update_technology_exogenous(
            scenario_id=self.scenario_id,
            technology_name=technology_name,
            parameter=parameter,
            region=region,
            sub_region=sub_region,
            sub_technology=sub_technology,
            subsidy=subsidy,
            transform=transform,
        )

    def update_endogenous_technology_variable(
        self,
        technology_name: str,
        parameter: str,
        transform: List[Transform],
        region: str,
        sub_region: Optional[str] = None,
        sub_technology: Optional[str] = None,
    ):
        return self.session.update_technology_endogenous(
            scenario_id=self.scenario_id,
            technology_name=technology_name,
            parameter=parameter,
            transform=transform,
            region=region,
            sub_region=sub_region,
            sub_technology=sub_technology,
        )

    def get_commodities(self, *args, **kwargs):
        return self.session.get_commodities(
            scenario_id=self.scenario_id, *args, **kwargs
        )

    def update_commodity_price(self, *args, **kwargs):
        return self.session.update_commodity_price(
            scenario_id=self.scenario_id, *args, **kwargs
        )
