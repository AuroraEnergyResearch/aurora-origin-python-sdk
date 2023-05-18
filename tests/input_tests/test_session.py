from origin_sdk.service.Scenario import Scenario
from origin_sdk.service.InputsEditor import InputsEditor
from tests.input_tests.utils_for_testing import (
    get_scenario_for_testing,
    testing_session as session,
)


def test_get_main_region():
    s = get_scenario_for_testing()
    ie = InputsEditor(s.scenario_id, session)
    assert (
        ie.inputs_session.get("productRegionInformation").get("code").lower() == "gbr"
    )

    s = Scenario.get_latest_scenario_from_region(session=session, region="deu")
    ie = InputsEditor(s.scenario_id, session)
    assert (
        ie.inputs_session.get("productRegionInformation").get("code").lower() == "deu"
    )
