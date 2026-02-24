---
sidebar_label: scenario_types
title: origin_sdk.types.scenario_types
---

The scenario_types module contains type hinting and can be useful when trying to
understand what options you have when interacting with functions, or what
outputs to expect from queries. Enums are available in
[scenario_enums](/docs/origin_sdk/types/scenario_enums) for import and usage.

## InputScenario Objects

```python
class InputScenario(TypedDict)
```

Interface for creating or updating scenarios. Note that while you may be
able to create a scenario partially, the values required to put it into a
launchable state varies based on configuration. If you are missing
parameters, the service ought to tell you what is missing.

**Attributes**:

- `projectGlobalId` _string_ - The ID of the project to create the scenario
  in
- `name` _string_ - The name of the scenario
- `baseScenarioGlobalId` _string_ - **Required only for non-Aurorean use.** The
  &quot;base&quot; scenario you wish to use. This is equivalent to your own
  scenario, or a published AER scenario that you wish to &quot;copy&quot;.
- `description` _optional, string_ - A description for the scenario. Purely for user
  purposes, not used by the system.
- `regionGroupCode` _optional, string_ - A region group for the scenario. Be aware
  that a &quot;regionGroup&quot; would be AUS, whereas a &quot;region&quot; would then be
  &quot;VIC&quot; or &quot;NSW&quot;. For most regions, the &quot;regionGroup&quot; and it&#x27;s three
  letter region code are identical.
- `useExogifiedInputs` _optional, boolean_ - A true value here is equivalent to the
  &quot;Model Determined Capacity&quot; toggled off in the interface. When this
  is set to false, the model automatically builds capacity to support
  demand. If you unselect this, you are choosing to take control of
  defining the capacity build assumptions (this runs much more
  quickly). Whether these options are available, depends on the
  scenario this is based on.
- `defaultCurrency` _optional, string_ - Should be set automatically once a
  `regionGroupCode` is chosen, but can be overridden
- `retentionPolicy` _optional, string_ - Internal only.
- `scenarioRunType` _optional, ScenarioRunType_ - **Deprecated for external use.**
  Internal only. External users should use `useExogifiedInputs` instead.
  Set useExogifiedInputs=True for MDC off (fixed capacities), or
  useExogifiedInputs=False for MDC on (model-determined capacities).
- `modelType` _optional, ModelType_ - Internal only.
- `modelPriceSpikiness` _optional, ModelPriceSpikiness_ - Used for AUS, set
  this to one of the ModelPriceSpikiness enum values if you wish to
  use the feature.
- `years` _optional, List[int]_ - Internal only.
- `weatherYear` _optional, int_ - The Weather Year for which to simulate (half)hourly profiles - if supported.
  Should only be used for scenarios with &quot;fixed capacities&quot; and without further edits; i.e.
  `useExogifiedInputs` = `True`, or `scenarioRunType` = `FYR`
- `advancedSettings` _optional, AdvancedScenarioSettings_ - Internal only.

## ScenarioSummaryType Objects

```python
class ScenarioSummaryType(TypedDict)
```

Dictionary received when requesting a list of scenarios

## RegionDict Objects

```python
class RegionDict(TypedDict)
```

Regional information object.

**Attributes**:

- `regionCode` _String_ - ISO code or similar from the service
- `metaUrl` _String_ - URL used to get the meta json file for this region&#x27;s downloads
- `dataUrlBase` _String_ - URL used as the base to construct a download URL
  for output data
- `__meta_json` _Optional_ - Not provided by the service. This field is
  populated as required by internal implementation of the Scenario class.
  Observe this at your own risk.

## ScenarioType Objects

```python
class ScenarioType(ScenarioSummaryType)
```

Extended scenario details received when requesting a single scenario
