---
sidebar_label: Scenario
title: origin_sdk.service.Scenario
---

## Scenario Objects

```python
class Scenario()
```

A Scenario class that holds state in order to provide a more Pythonic
interface for Scenario building and downloading outputs

**Arguments**:

- `scenario_id` _str_ - The ID to initialise the scenario with. Will fetch
  the scenario details and populate itself with details
- `session` _OriginSession_ - You should first instantiate an OriginSession
  and pass this over to the Scenario.
  
  Properties:
- `scenario_id` _str_ - The scenario ID
- `session` _OriginSession_ - The OriginSession attached to this scenario
- `scenario` _ScenarioType_ - The full Scenario object from the service
  

**Methods**:

  get_downloadable_regions()

#### get\_downloadable\_regions

```python
def get_downloadable_regions()
```

A helper function to return the regions available for download from
this scenario

**Returns**:

  A list of regions available

#### get\_meta\_json

```python
def get_meta_json(region: str)
```

A helper function that gets the meta json for the region. Caches into
internal state for future use.

**Returns**:

  A meta json useful for downloading files.

#### get\_download\_types

```python
def get_download_types(region: str)
```

Returns the types and granularities of download available for the region. Expect something
like &quot;system&quot;|&quot;technology&quot; and &quot;1y&quot;|&quot;1m&quot; for type and granularity
respectively.

**Arguments**:

  region (String)
  

**Returns**:

  A list of type and granularity downloads available for the region.

#### download\_output\_csv

```python
def download_output_csv(region: str,
                        type: str,
                        granularity: str,
                        currency: str,
                        outfile: Optional[str] = None)
```

Downloads a csv from the service. As of writing, returns the CSV
directly from the function. Do not use this for half hourly data in it&#x27;s
current form, it&#x27;s a bad idea.

**Arguments**:

- `region` _String_ - The region to download for. Use
  &quot;get_downloadable_regions&quot; to see a list of options.
- `type` _String_ - The &quot;type&quot; of file to download. You can use
  &quot;get_download_types&quot; to query the available options.
- `granularity` _String_ - The &quot;granularity&quot; of file to download. You can use
  &quot;get_download_types&quot; to query the available options.
- `currency` _String_ - The currency year to download the file in.
  

**Returns**:

  CSV as text

#### refresh

```python
def refresh()
```



