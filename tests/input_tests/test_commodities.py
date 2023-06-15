from origin_sdk.OriginSession import OriginSession

from tests.input_tests.utils_for_testing import get_test_scenario_for_reading


def test_can_get_commodities():
    o = OriginSession()
    s = get_test_scenario_for_reading()
    cmdty = o.get_commodities(s.scenario_id)

    assert cmdty is not None
