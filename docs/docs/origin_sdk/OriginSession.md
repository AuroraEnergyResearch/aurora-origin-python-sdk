---
sidebar_label: OriginSession
title: origin_sdk.OriginSession
---

## OriginSession Objects

```python
class OriginSession(APISession)
```

Manage access to the Origin API.

By default the session will connect to the production Origin API endpoint.
This can be overridden by passing the base_url into the constructor or by
setting the above environment variables for BASE_URLs. This feature is for
internal use only.

The authentication token is read from the users home directory
*$home/.aurora-api-key* e.g. *C:/Users/Joe Bloggs/.aurora-api-key*. This can
be overridden by passing the token into the constructor or by setting the
environment variable *AURORA_API_KEY*.

**Arguments**:

- `token` _string, optional_ - Override the api authentication token used for
  API access. Defaults to None.
- `scenario_base_url` _string, optional_ - Override the scenario service base url
- `inputs_base_url` _string, optional_ - Override the model inputs service base url

#### get\_aurora\_scenarios

```python
def get_aurora_scenarios(region: Optional[str] = None,
                         query_filter=None) -> List[ScenarioSummaryType]
```



#### get\_scenario\_by\_id

```python
def get_scenario_by_id(scenario_id: str) -> ScenarioType
```



#### create\_scenario

```python
def create_scenario(scenario) -> ScenarioType
```



#### update\_scenario

```python
def update_scenario(scenario_update) -> ScenarioType
```



#### delete\_scenario

```python
def delete_scenario(scenario_id: str)
```



#### launch\_scenario

```python
def launch_scenario(scenario_id: str) -> ScenarioType
```



#### get\_projects

```python
def get_projects() -> List[ProjectSummaryType]
```



#### get\_project

```python
def get_project(project_id: str) -> ProjectType
```



#### create\_project

```python
def create_project(project) -> ProjectSummaryType
```



#### update\_project

```python
def update_project(project_update) -> ProjectSummaryType
```



#### delete\_project

```python
def delete_project(project_id)
```



#### pin\_project

```python
def pin_project(project_id)
```



#### unpin\_project

```python
def unpin_project(project_id)
```



