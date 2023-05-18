from origin_sdk.OriginSession import OriginSession
from origin_sdk.service.Scenario import Scenario


testing_session = OriginSession()

test_scenario = None


def get_scenario_for_testing():
    global test_scenario
    if test_scenario is None:
        test_scenario = Scenario.get_latest_scenario_from_region(
            session=testing_session, region="gbr"
        )

    return test_scenario
