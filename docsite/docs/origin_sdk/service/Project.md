---
sidebar_label: Project
title: origin_sdk.service.Project
---

## Project Objects

```python
class Project()
```

The Project class is a more user-friendly set of mappings around the
lower level OriginSession calls.

#### get

```python
def get(key: str)
```

Shortcut for Project.project.get()

#### refresh

```python
def refresh()
```

Refreshes the project data.

#### pin

```python
def pin()
```

Pins the project, if it isn&#x27;t already

#### unpin

```python
def unpin()
```

Unpins the project, if it isn&#x27;t already

#### create\_scenario

```python
def create_scenario(scenario_opts: InputScenario) -> Scenario
```

Shortcut to create a scenario in this project. See
OriginSession.createScenario for info on argument `scenario_opts`

#### get\_scenario\_by\_name

```python
def get_scenario_by_name(scenario_name: str) -> Scenario
```

Gets a scenario from the current project using the name instead of an
ID.

NOTE: In the case of more than one scenario with the same name, the
first one will be returned as ordered by the service.

#### get\_or\_create\_scenario\_by\_name

```python
def get_or_create_scenario_by_name(scenario_name: str,
                                   base_scenario_id: str) -> Scenario
```

Either gets a scenario from this project or creates a scenario in
this project with the name specified. In the case of create, requires a
base_id.

NOTE: In the case of more than one scenario with the same name, the
first one will be returned as ordered by the service.

**Arguments**:

- `scenario_name` - str - The name of the scenario to look for
- `base_id` - str - The ID of the scenario to use as a base in the case
  that the scenario doesn&#x27;t exist

#### get\_project\_by\_name

```python
@staticmethod
def get_project_by_name(session: OriginSession, name: str) -> "Project"
```

Gets a project using the name instead of an ID.

NOTE: In the case of more than one project with the same name, the
first one will be returned as ordered by the service.

#### get\_or\_create\_project\_by\_name

```python
@staticmethod
def get_or_create_project_by_name(session: OriginSession,
                                  name: str,
                                  pin_project: bool = False) -> "Project"
```

Either creates a project with this name, or returns the project that
already exists with the same name.

NOTE: In the case of more than one project with the same name, the
first one will be returned as ordered by the service.

**Arguments**:

- `session` - OriginSession - The session to make API calls with
- `name` - str - The name of the project to find/create
- `pin_project` - Optional, bool - Whether to pin the project if it&#x27;s not
  already, defaults to False

