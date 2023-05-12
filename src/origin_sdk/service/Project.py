import logging
from origin_sdk.OriginSession import OriginSession
from typing import Optional

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
        if not self.project.get("isProjectPinned"):
            self.session.pin_project(self.project_id)
        return self

    def unpin(self):
        """Unpins the project, if it isn't already"""
        if self.project.get("isProjectPinned"):
            self.session.unpin_project(self.project_id)
        return self

    def get_or_create_scenario_by_name(
        self, scenario_name: str, base_scenario_id: Optional[str] = None
    ):
        """Either gets a scenario from this project or creates a scenario in
        this project with the name specified. In the case of create, requires a
        base_id.

        Arguments:
            scenario_name: str - The name of the scenario to look for
            base_id: Optional, str - The ID of the scenario to use as a base
        """
        self.refresh()

        scenarios = [
            scenario
            for scenario in self.project.get("scenarios")
            if scenario.get("name").lower() == scenario_name.lower()
        ]

        scenario = None
        if len(scenarios) > 0:
            # We found a scenario with a name match!
            # Select it to return
            scenario = scenarios[0]
        elif base_scenario_id is not None:
            # No scenario found, create it.
            scenario = self.session.create_scenario(
                {
                    "projectGlobalId": self.project.get("projectGlobalId"),
                    "baseScenarioGlobalId": base_scenario_id,
                    "name": scenario_name,
                }
            )
        else:
            logger.warn(
                (
                    "No scenario found in project ",
                    f"{self.project.get('name')}",
                    f"' with name '{scenario_name}'",
                )
            )

        return scenario

    @staticmethod
    def get_or_create_project_by_name(
        session: OriginSession, name: str, pin_project: bool = False
    ):
        """Either creates a project with this name, or returns the project that
        already exists with the same name. In the event there is more than one
        project, returns the first one returned by the service.

        Arguments:
            session: OriginSession - The session to make API calls with
            name: str - The name of the project to find/create
            pin_project: Optional, bool - Whether to pin the project if it's not
            already, defaults to False
        """

        all_projects = [p for p in session.get_projects() if p.get("name") == name]

        if len(all_projects) > 0:
            project = all_projects[0]
        else:
            project = session.create_project({"name": name})

        if project.get("isProjectPinned") is False and pin_project is True:
            session.pin_project(project.get("projectGlobalId"))

        return Project(session=session, project_id=project.get("projectGlobalId"))
