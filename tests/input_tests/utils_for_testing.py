from typing import Optional
from origin_sdk.OriginSession import OriginSession
from origin_sdk.service.Scenario import Scenario
from origin_sdk.service.Project import Project
from pytest import fixture
from uuid import uuid4


testing_session = OriginSession()

readonly_test_scenario = None
test_project = None


@fixture(scope="session", autouse=True, name="project")
def setup_test_project():
    global test_project
    test_project = Project.get_or_create_project_by_name(
        testing_session,
        f"Pytest project for SDK {uuid4()}",
        create_config={"productId": "SaaS"},
    )

    yield test_project

    testing_session.delete_project(test_project.project_id)


# Not sure I want this to be a fixture, will the scenarios I set up always be
# the same?
# @fixture(scope="function", autouse=True, name="scenario")
# def get_scenario_for_update_tests():
#     Scenario.


def get_test_scenario_for_reading():
    global readonly_test_scenario
    if readonly_test_scenario is None:
        readonly_test_scenario = Scenario.get_latest_scenario_from_region(
            session=testing_session, region="gbr", name_filter="central"
        )

    return readonly_test_scenario


def get_copy_of_readonly_scenario_for_updating(name: Optional[str] = None):
    ro_scenario = get_test_scenario_for_reading()
    if test_project is not None:
        s = test_project.create_scenario(
            {
                "name": f"test scenario: {name}",
                "baseScenarioGlobalId": ro_scenario.scenario_id,
            }
        )
        return s
