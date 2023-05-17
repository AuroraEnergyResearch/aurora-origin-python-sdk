from origin_sdk.OriginSession import OriginSession
from origin_sdk.service.Scenario import Scenario
from origin_sdk.service.InputsEditor import InputsEditor


session = OriginSession()

test_scenario = None


def get_scenario_for_testing(region: str = "gbr"):
    global test_scenario
    if test_scenario is None:
        test_scenario = Scenario.get_latest_scenario_from_region(
            session=session, region=region
        )

    return test_scenario


def test_get_main_region():
    s = get_scenario_for_testing("gbr")
    ie = InputsEditor(s.scenario_id, session)
    assert ie.session.
    pass


def test_get_technology_names():
    s = get_scenario_for_testing()
    ie = InputsEditor(s.scenario_id, session)

    techs = ie.get_technology_names()

    assert techs is not None
