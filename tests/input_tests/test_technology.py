from origin_sdk.service.InputsEditor import InputsEditor
from tests.input_tests.utils_for_testing import (
    get_scenario_for_testing,
    testing_session as session,
)


def test_get_technology_names():
    s = get_scenario_for_testing()
    ie = InputsEditor(s.scenario_id, session)

    techs = ie.get_technology_names()

    assert techs is not None
