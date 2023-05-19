from origin_sdk.gql.queries.input_queries.session import create_get_session_gql
from origin_sdk.gql.queries.input_queries.utils import variable_values_with_transform


get_demand_regions_gql = create_get_session_gql({}, {"getDemand": {"region": None}})

original_value_only = {"original": None}

get_demand_gql = create_get_session_gql(
    {"demandFilter": "GetDemandFilterDemandInput"},
    {
        "getDemand (filter: $demandFilter)": {
            "region": None,
            "peakLoadDemand": None,
            "variables": {"year": None, "totalDemand": variable_values_with_transform},
            "technologies": {
                **{
                    key: original_value_only
                    for key in ["region", "technology", "originTechnology"]
                },
                "variables": {
                    "year": None,
                    "totalDemand": variable_values_with_transform,
                },
            },
        }
    },
)
