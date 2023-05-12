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

The authentication token is read from the user&#x27;s home directory
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
def get_aurora_scenarios(
        region: Optional[str] = None) -> List[ScenarioSummaryType]
```

Gets a list of all published Aurora scenarios.

**Arguments**:

  region (string, optional) - A regional filter. We accept three
  letter ISO codes where appropriate. If in doubt as to which code to
  use for a region (e.g. Iberia), you can check the Origin URL while
  browsing the platform. You will see something like
  &quot;.../launcher/aer/&lt;REGION&gt;&quot;
  

**Returns**:

  List[ScenarioSummaryType]

#### get\_scenario\_by\_id

```python
def get_scenario_by_id(scenario_id: str) -> ScenarioType
```

Get a single scenario by it&#x27;s ID.

**Arguments**:

  scenario_id (string) - The ID of the scenario
  

**Returns**:

  ScenarioType

#### create\_scenario

```python
def create_scenario(scenario: InputScenario) -> ScenarioType
```

Creates a new scenario

**Arguments**:

  scenario (InputScenario) -

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
def create_project(project: InputProject) -> ProjectSummaryType
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



#### get\_meta\_json

```python
def get_meta_json(meta_url: str)
```



#### get\_inputs\_session

```python
def get_inputs_session(scenario_id: str)
```

Gets the inputs instance information, as well as rehydrating all the
data if required

#### get\_technology\_names

```python
def get_technology_names(scenario_id: str)
```

Gets the technology names available for update, by region, and any
subtechnology groupings

#### get\_technology

```python
def get_technology(scenario_id: str,
                   technology_name: str,
                   region: str,
                   subregion: Optional[str] = None,
                   exogenous_sub_technology: Optional[str] = None,
                   subsidy: Optional[str] = None,
                   endogenous_sub_technology: Optional[str] = None)
```

Gets a specific technology information and all it&#x27;s yearly and non
yearly values available for update

#### update\_technology\_endogenous

```python
def update_technology_endogenous(scenario_id: str,
                                 technology_name: str,
                                 parameter: str,
                                 transform: List[Transform],
                                 region: str,
                                 sub_region: Optional[str] = None,
                                 sub_technology: Optional[str] = None)
```

Updates an endogenous technology assumption.

#### update\_technology\_exogenous

```python
def update_technology_exogenous(scenario_id: str,
                                technology_name: str,
                                parameter: str,
                                transform: List[Transform],
                                region: str,
                                sub_region: Optional[str] = None,
                                subsidy: Optional[str] = None,
                                sub_technology: Optional[str] = None)
```

Updates an exogenous technology assumption.

