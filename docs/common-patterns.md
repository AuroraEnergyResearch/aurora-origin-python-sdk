# Common Patterns

Representative examples for getting started with the Origin SDK.

```{contents}
:local:
:depth: 2
```

## Get projects

```python
session = OriginSession()

# Get projects
session.get_projects()
```

## Get scenarios for a region

```python
session = OriginSession()

# Get published scenarios for a region
session.get_aurora_scenarios(region="gbr")
```

## Get latest Central case

```python
from datetime import datetime


def get_latest_central_for(region: str):
    # First, get regional scenarios
    scenarios_for_region = (
        session.get_aurora_scenarios(region=region)
        .get("data")
        .get("getScenarios")
    )

    # Filter to central cases only
    central_cases = [
        scenario
        for scenario in scenarios_for_region
        if "central" in scenario.get("name").lower()
    ]

    # Sort using publication date
    central_cases.sort(
        key=lambda scenario: datetime.fromisoformat(
            scenario["publicationDate"]
        ).timestamp(),
        reverse=True,
    )

    return central_cases[0]


# Call function, getting latest case for AUS
get_latest_central_for("aus")
```
