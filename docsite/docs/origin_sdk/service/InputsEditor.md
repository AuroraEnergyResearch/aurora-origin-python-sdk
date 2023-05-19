---
sidebar_label: InputsEditor
title: origin_sdk.service.InputsEditor
---

## InputsEditor Objects

```python
class InputsEditor()
```

-- BETA --

Not suitable for wide consumption yet, preliminary user-friendly wrapper around
the Inputs Service API calls.

WARNING: If using, the contract defined here is subject to change.

#### get\_demand\_regions

```python
def get_demand_regions()
```

Gets the regios available for get/update demand functionality in
A Origin. Regional availability is affected by the &quot;main region&quot; the scenario has been
configured to run.

#### get\_demand\_technologies

```python
def get_demand_technologies()
```

Gets all the demand techs and the data for them

#### get\_technology\_names

```python
def get_technology_names() -> TechnologyNames
```

Gets the technology names available for use in get/update technology
functionality in Origin.

Caches into the state of the instance for ease of use.

**Returns**:

  TechnologyNames object (see types.input_types for details) General
  structure is as follows: {
- `[region]` - {
- `[technologyName]` - {
- `subTechnologiesExogenous` - List[str],
- `subTechnologiesEndogenous` - List[str], subRegions: {
- `[subregion]` - {
- `subsidies` - List[str] subTechnologiesExogenous:
  List[str], subTechnologiesEndogenous: List[str],
  }
  }
  }
  }
  }

