from origin_sdk.OriginSession import OriginSession
from origin_sdk.service.Scenario import Scenario
from origin_sdk.service.Project import Project
from uuid import uuid4
from origin_sdk.types.error_types import ProjectNotFound, ScenarioNotFound

localhost_testing = {
    "scenario_base_url": "http://localhost:3001",
    "token": "OriginAdvancedUser",
}

session = OriginSession()

test_project = None


def get_project_for_testing():
    global test_project
    if test_project is None:
        test_project = Project.get_or_create_project_by_name(
            session=session, name=f"testing for SDK {str(uuid4())}"
        )
    return test_project


def get_project_by_name_throws_correct_error():
    try:
        Project.get_project_by_name(session=session, name=str(uuid4()))
        assert False

    except ProjectNotFound:
        assert True


def test_get_or_create_doesnt_create_more():
    p1 = get_project_for_testing()
    p2 = Project.get_or_create_project_by_name(session=session, name=p1.get("name"))

    assert p1.project_id == p2.project_id


def test_get_scenario_by_name_throws_correct_error():
    p1 = get_project_for_testing()
    try:
        p1.get_scenario_by_name(scenario_name=str(uuid4()))
        assert False

    except ScenarioNotFound:
        assert True


def test_get_or_create_scenario_by_name_gets_before_creates():
    p1 = get_project_for_testing()
    latest_gb = Scenario.get_latest_scenario_from_region(session, "gbr")
    unique_name = str(uuid4())

    # Create a new scenario in the project
    p1.create_scenario(
        {"name": unique_name, "baseScenarioGlobalId": latest_gb.scenario_id}
    )

    # Get or Create a scenario by name
    p1.get_or_create_scenario_by_name(
        scenario_name=unique_name, base_scenario_id=latest_gb.scenario_id
    )

    # Assert only one exists
    p1.refresh()
    assert len(p1.get("scenarios")) == 1

    # Create another one, using a new unique ID
    p1.get_or_create_scenario_by_name(
        scenario_name=str(uuid4()), base_scenario_id=latest_gb.scenario_id
    )

    # Assert two exist
    p1.refresh()
    assert len(p1.get("scenarios")) == 2

    # Cleanup
    [
        session.delete_scenario(scenario.get("scenarioGlobalId"))
        for scenario in p1.get("scenarios")
    ]


def test_projects_pin_and_unpin():
    p1 = get_project_for_testing()
    p1.pin().refresh()

    assert p1.get("isProjectPinned") is True

    p1.unpin().refresh()

    assert p1.get("isProjectPinned") is False
