from origin_sdk.service.Scenario import Scenario
from origin_sdk.service.InputsEditor import InputsEditor
from .utils_for_testing import (
    get_default_test_scenario_for_reading,
    testing_session as session,
)


def test_get_main_region():
    s = get_default_test_scenario_for_reading()
    ie = InputsEditor(s.scenario_id, session)
    assert (
        ie.inputs_session.get("productRegionInformation").get("code").lower() == "gbr"
    )

    s = Scenario.get_latest_scenario_from_region(session=session, region="deu")
    ie = InputsEditor(s.scenario_id, session)
    assert (
        ie.inputs_session.get("productRegionInformation").get("code").lower() == "deu"
    )


def test_get_session_transforms():
    s = get_default_test_scenario_for_reading()
    ie = InputsEditor(s.scenario_id, session)
    ie_session = ie.inputs_session
    assert ie_session.get("transforms") is not None
