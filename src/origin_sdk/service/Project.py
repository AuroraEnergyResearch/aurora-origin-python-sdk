import logging
from origin_sdk.OriginSession import OriginSession
from typing import Optional
from origin_sdk.service.Scenario import Scenario
from origin_sdk.types.error_types import ProjectNotFound, ScenarioNotFound
from origin_sdk.types.project_types import InputProject

from origin_sdk.types.scenario_types import InputScenario

logger = logging.getLogger(__name__)


class Project:
    """The Project class is a more user-friendly set of mappings around the
    lower level OriginSession calls."""

    def __init__(self, project_id: str, session: OriginSession):
        self.project_id = project_id
        self.session = session
        self.project = self.session.get_project(project_id)

    def get(self, key: str):
        """
        Shortcut for Project.project.get()
        """
        return self.project.get(key)

    def refresh(self):
        """Refreshes the project data."""
        self.project = self.session.get_project(self.project_id)
        return self

    def pin(self):
        """Pins the project, if it isn't already"""
        if self.project.get("isProjectPinned") is not True:
            self.session.pin_project(self.project_id)
        return self

    def unpin(self):
        """Unpins the project, if it isn't already"""
        if self.project.get("isProjectPinned") is True:
            self.session.unpin_project(self.project_id)
        return self

    def create_scenario(self, scenario_opts: InputScenario) -> Scenario:
        """Shortcut to create a scenario in this project. See
        OriginSession.createScenario for info on argument `scenario_opts`"""
        scenario = self.session.create_scenario(
            {"projectGlobalId": self.project_id, **scenario_opts}
        )
        return Scenario(
            session=self.session, scenario_id=scenario.get("scenarioGlobalId")
        )

    def get_scenario_by_name(self, scenario_name: str) -> Scenario:
        """Gets a scenario from the current project using the name instead of an
        ID.

        NOTE: In the case of more than one scenario with the same name, the
        first one will be returned as ordered by the service."""

        self.refresh()

        scenarios = [
            scenario
            for scenario in self.project.get("scenarios")
            if scenario.get("name").lower() == scenario_name.lower()
        ]

        if len(scenarios) > 0:
            # We found a scenario with a name match!
            # Select it to return
            return Scenario(
                session=self.session, scenario_id=scenarios[0].get("scenarioGlobalId")
            )
        else:
            raise ScenarioNotFound(
                f"No scenario with {scenario_name.lower()} in project {self.project.get('name')}"
            )

    def get_or_create_scenario_by_name(
        self, scenario_name: str, base_scenario_id: str
    ) -> Scenario:
        """Either gets a scenario from this project or creates a scenario in
        this project with the name specified. In the case of create, requires a
        base_id.

        NOTE: In the case of more than one scenario with the same name, the
        first one will be returned as ordered by the service.

        Arguments:
            scenario_name: str - The name of the scenario to look for
            base_id: str - The ID of the scenario to use as a base in the case
            that the scenario doesn't exist
        """

        scenario = None

        try:
            scenario = self.get_scenario_by_name(scenario_name=scenario_name)

        except ScenarioNotFound:
            # No scenario found, create it.
            scenario = self.create_scenario(
                {
                    "baseScenarioGlobalId": base_scenario_id,
                    "name": scenario_name,
                }
            )

        return scenario

    @staticmethod
    def get_project_by_name(session: OriginSession, name: str) -> "Project":
        """Gets a project using the name instead of an ID.

        NOTE: In the case of more than one project with the same name, the
        first one will be returned as ordered by the service."""

        all_projects = [p for p in session.get_projects() if p.get("name") == name]

        if len(all_projects) > 0:
            project = all_projects[0]
            return Project(session=session, project_id=project.get("projectGlobalId"))

        else:
            raise ProjectNotFound(f"No project found containing '{name}'")

    @staticmethod
    def create(session: OriginSession, project: InputProject) -> "Project":
        created_project = session.create_project(project=project)
        return Project(
            session=session, project_id=created_project.get("projectGlobalId")
        )

    @staticmethod
    def get_or_create_project_by_name(
        session: OriginSession, name: str, pin_project: bool = False
    ) -> "Project":
        """Either creates a project with this name, or returns the project that
        already exists with the same name.

        NOTE: In the case of more than one project with the same name, the
        first one will be returned as ordered by the service.

        Arguments:
            session: OriginSession - The session to make API calls with
            name: str - The name of the project to find/create
            pin_project: Optional, bool - Whether to pin the project if it's not
            already, defaults to False
        """
        try:
            project = Project.get_project_by_name(session=session, name=name)

        except ProjectNotFound:
            project = session.create_project({"name": name})

        new_project = Project(
            session=session, project_id=project.get("projectGlobalId")
        )

        if pin_project is True:
            new_project.pin()

        return new_project
