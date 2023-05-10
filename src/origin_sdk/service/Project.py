import logging
from origin_sdk.OriginSession import OriginSession
from typing import Optional
from tempfile import TemporaryDirectory
import pandas as pd
from io import StringIO

logger = logging.getLogger(__name__)


class Project:
    def __init__(self, project_id: str, session: OriginSession):
        self.project_id = project_id
        self.session = session
        self.project = self.session.get_project(project_id)

    def get(self, key: str):
        """
        Shortcut for Project.project.get()
        """
        return self.project.get(key)

    def pin(self):
        if not self.project.get("isProjectPinned"):
            self.session.pin_project(self.project_id)

    def unpin(self):
        if self.project.get("isProjectPinned"):
            self.session.unpin_project(self.project_id)
