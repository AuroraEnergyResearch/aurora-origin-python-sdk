from origin_sdk.service.InputsEditor import InputsEditor
from origin_sdk.service.Scenario import Scenario
from tests.input_tests.utils_for_testing import (
    get_scenario_for_testing,
    testing_session as session,
)


def test_get_demand_regions():
    s = get_scenario_for_testing()
    ie = InputsEditor(s.scenario_id, session)

    regs = ie.get_demand_regions()

    assert regs is not None


def test_get_demand():
    s = get_scenario_for_testing()
    s = Scenario.get_latest_scenario_from_region(session, "gbr", name_filter="central")
    ie = InputsEditor(s.scenario_id, session)

    regs = ie.get_demand_regions()

    for reg in regs:
        dem = ie.get_demand_for_region(region=reg)
        assert dem is not None

        dem_techs = dem.get("technologies")
        assert dem_techs is not None
