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
def get_inputs_session(scenario_id: str) -> InputsSession
```

Gets the inputs instance information, as well as rehydrating all the
data if required

#### get\_technology\_names

```python
@access_next_data_key_decorator
def get_technology_names(scenario_id: str) -> TechnologyNames
```

Gets the technology names available for update, by region, and any
subtechnology groupings

#### get\_technology

```python
@access_next_data_key_decorator
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
@access_next_data_key_decorator
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
@access_next_data_key_decorator
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

#### get\_demand\_regions

```python
def get_demand_regions(scenario_id: str) -> List[str]
```

Gets the regions of demand available for the current scenario

#### get\_demand

```python
@access_next_data_key_decorator
def get_demand(
        scenario_id: str,
        demand_filter: Optional[InputsDemandFilter] = None
) -> List[InputsDemand]
```

Gets system demand and demand technology assumptions for this scenario

#### update\_system\_demand

```python
@access_next_data_key_decorator
def update_system_demand(scenario_id: str,
                         region: str,
                         variable: str,
                         transform: List[Transform],
                         auto_capacity_market_target: Optional[bool] = None)
```

Updates a system demand parameter (one that appears under variables
of the main demand object, and not one of the demand technologies variables).

#### get\_demand\_technology\_names

```python
@access_next_data_key_decorator
def get_demand_technology_names(
        scenario_id: str,
        demand_technology_filter: Optional[Any] = None) -> List[InputsDemand]
```

Gets just demand technology names available, as well as the regions
they each belong to.

#### get\_demand\_technologies

```python
@access_next_data_key_decorator
def get_demand_technologies(
        scenario_id: str,
        demand_technology_filter: Optional[Any] = None) -> List[InputsDemand]
```

Gets just demand technologies, without system demand information.

#### update\_demand\_technology\_variable

```python
@access_next_data_key_decorator
def update_demand_technology_variable(
        scenario_id: str,
        region: str,
        technology: str,
        variable: str,
        transform: List[Transform],
        auto_capacity_market_target: Optional[bool] = None
) -> List[InputsDemand]
```

Updates a demand technology variable (one that appears on a
demand technology object, rather than on the system level demand
object).

#### get\_commodities

```python
@access_next_data_key_decorator
def get_commodities(scenario_id: str,
                    native_units_flag: Optional[bool] = None,
                    regions: Optional[List[str]] = None,
                    commodities: Optional[List[str]] = None)
```

Gets commodities data.

**Arguments**:

- `scenario_id` _String_ - ID of the scenario to get the commodities data from
- `native_units_flag` _Optional, Boolean_ - What units should be used
  on the return data, MWh or the &quot;native units&quot; the commodities
  come in. Defaults to false.
- `regions` _Optional, List[String]_ - If given, will filter the
  commodity prices to the region specifically. By default, we will
  perform an equally weighted global average.
- `commodities` _Optional, List[String]_ - If given, will filter the
  commodities to the ones specified. By default, we will
  query for all commodities.

#### update\_commodity\_price

```python
@access_next_data_key_decorator
def update_commodity_price(scenario_id: str,
                           commodity: str,
                           regions: List[str],
                           transform: List[Transform],
                           native_units_flag: Optional[bool] = None)
```

Updates a commodity price.

**Arguments**:

- `scenario_id` _String_ - ID of the scenario to get the commodities data from
  come in. Defaults to false.
- `commodity` _String_ - The commodity to update.
- `regions` _List[String]_ - The regions to update. You can use the
  regions array on the &quot;get commodities&quot; return object to inform the
  view you should update.
- `transform` _List[Transform]_ - The transform array used in all updates
- `native_units_flag` _Optional, Boolean_ - What units should be used
  on the return data, MWh or the &quot;native units&quot; the commodities

#### change\_base\_commodities\_assumptions

```python
@access_next_data_key_decorator
def change_base_commodities_assumptions(scenario_id: str,
                                        rebase_reference_id: str)
```

Function to change the underlying commodities assumptions. This
changes the *original* values, and then any changes you have made (e.g.
+15%) will apply over the top.

#### get\_interconnectors\_connections

```python
@access_next_data_key_decorator
def get_interconnectors_connections(scenario_id: str) -> Dict[str, List[str]]
```

Gets a dictionary of interconnector connections between regions for
the given scenario.

**Arguments**:

- `scenario_id` _String_ - ID of the scenario to get the interconnector data from

#### get\_interconnectors

```python
@access_next_data_key_decorator
def get_interconnectors(scenario_id: str, region: str, connection_region: str)
```

Gets the interconnector data between two regions.

**Arguments**:

- `scenario_id` _String_ - ID of the scenario to get the interconnector data from
- `region` _String_ - The region the interconnector is to/from
- `connection_region` _String_ - The connected region the interconnector is from/to

#### update\_interconnectors

```python
@access_next_data_key_decorator
def update_interconnectors(scenario_id: str, from_region: str, to_region: str,
                           variable: str, transform: List[Transform])
```

Function to update a interconnector variable between two regions.

**Arguments**:

- `scenario_id` _String_ - ID of the scenario to update the interconnector data from
- `from_region` _String_ - The region the interconnector is from
- `to_region` _String_ - The region the interconnector is to
- `variable` _String_ - The variable to update
- `transform` _List[Transform]_ - The transform array used in all updates

