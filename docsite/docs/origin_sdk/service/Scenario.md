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

**Attributes**:

- `scenario_id` _str_ - The scenario ID
- `session` _OriginSession_ - The OriginSession attached to this scenario
- `scenario` _ScenarioType_ - The full Scenario object from the service

#### get_downloadable_regions

```python
def get_downloadable_regions()
```

A helper function to return the regions available for download from
this scenario

**Returns**:

A list of regions available

#### get_scenario_regions

```python
def get_scenario_regions()
```

Helper function to get the regions object on the Scenario, as it&#x27;s a
common access pattern.

#### get_scenario_region

```python
def get_scenario_region(region: str)
```

Helper function to get a specific region from the regions object, as
it&#x27;s a common access pattern.

**Returns**:

RegionDict

#### get_download_types

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

#### get_scenario_data_csv

```python
def get_scenario_data_csv(region: str,
                          download_type: str,
                          granularity: str,
                          currency: Optional[str] = None,
                          force_no_cache: bool = False,
                          params: Optional[dict[str, str]] = None)
```

Downloads a csv from the service and returns as a string. Recommended to
use if looking to generate a csv file on disk.

In general, our csvs have two header rows. The first identifies the
column of data and the second is a unit string or other contextual
information if relevant. To convert this to a pandas data frame,
pass the output of this method to pandas&#x27; read_csv() method via a buffer.

**Example**:

```python
  csv_data = scenario.get_scenario_data_csv("gbr", "system", "1y")
  buffer = StringIO(csv_data)
  df = pd.read_csv(buffer, header=[0,1])
```

**Arguments**:

- `region` _String_ - The region to download for. Use
  &quot;get_downloadable_regions&quot; to see a list of options.
- `type` _String_ - The &quot;type&quot; of file to download. You can use
  &quot;get_download_types&quot; to query the available options.
- `granularity` _String_ - The &quot;granularity&quot; of file to download. You can use
  &quot;get_download_types&quot; to query the available options.
- `currency` _Optional, String_ - The currency year to download the file
  in. Will default to `defaultCurrency` on the scenario if available.

**Returns**:

CSV as text string

#### get_scenario_dataframe

```python
def get_scenario_dataframe(region: str,
                           download_type: str,
                           granularity: str,
                           currency: Optional[str] = None,
                           force_no_cache: bool = False,
                           params: Optional[dict[str, str]] = None)
```

This method is deprecated. Use get_scenario_data_csv instead.

**Example**:

```python
  csv_data = scenario.get_scenario_data_csv("gbr", "system", "1y")
  buffer = StringIO(csv_data)
  df = pd.read_csv(buffer, header=[0,1])
```

---

Much the same as `get_scenario_data` but instead parses the CSV as a
pandas data frame for easier consumption via a script. In general, our
CSVs have two header rows. The first identifies the column of data and
the second is a unit string or other contextual information if relevant.

**Arguments**:

- `region` _String_ - The region to download for. Use
  &quot;get_downloadable_regions&quot; to see a list of options.
- `type` _String_ - The &quot;type&quot; of file to download. You can use
  &quot;get_download_types&quot; to query the available options.
- `granularity` _String_ - The &quot;granularity&quot; of file to download. You can use
  &quot;get_download_types&quot; to query the available options.
- `currency` _Optional, String_ - The currency year to download the file
  in. Will default to `defaultCurrency` on the scenario if available.

**Returns**:

Pandas Dataframe

#### refresh

```python
def refresh()
```

Contacts the service to get an updated view of the scenario. Useful for
things such as polling on a frequency.

#### get

```python
def get(key: str)
```

Shortcut for Scenario.scenario.get()

#### get_latest_scenario_from_region

```python
@staticmethod
def get_latest_scenario_from_region(
        session: OriginSession,
        region: str,
        name_filter: Optional[Union[str, List[str]]] = None)
```

Given a region (and optional name match) will return the latest
scenario found.
