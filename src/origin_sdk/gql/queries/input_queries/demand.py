from typing import Any, List
from origin_sdk.gql.queries.input_queries.config import get_demand_variables_from_config
from origin_sdk.gql.queries.input_queries.session import create_get_session_gql
from origin_sdk.gql.queries.input_queries.tech_demand import create_demand_tech_tree
from origin_sdk.gql.queries.input_queries.utils import (
    RecursiveTree,
    tree_to_string,
    variable_values_with_transform,
)


get_demand_regions_gql = create_get_session_gql({}, {"getDemand": {"region": None}})


def create_demand_query_tree(system: List[str], tech: List[str]) -> RecursiveTree:
    return {
        "region": None,
        "peakLoadDemand": None,
        "variables": {
            "year": None,
            **{variable: variable_values_with_transform for variable in system},
        },
        "technologies": create_demand_tech_tree(tech),
    }


def get_demand_gql(demand_config: Any):
    return create_get_session_gql(
        {
            "demandFilter": "GetDemandFilterDemandInput",
            "aggregateRegions": "Boolean",
        },
        {
            "getDemand (filter: $demandFilter, aggregateRegions: $aggregateRegions)": create_demand_query_tree(
                *get_demand_variables_from_config(demand_config)
            ),
        },
    )


def update_system_demand_gql(demand_config: Any):
    demand_tree = create_demand_query_tree(
        *get_demand_variables_from_config(demand_config)
    )
    return f"""mutation (
    $sessionId: String!,
    $technology: EnumDemandTechnology,
    $region: ModelRegion,
    $regions: [ModelRegion!],
    $variable: String!,
    $autoCapacityMarketTarget: Boolean,
    $tx: [YearlyNumberItemInput]!
) {{
    updateDemandVariable (
        sessionId: $sessionId,
        variable: $variable,
        technology: $technology,
        region: $region,
        regions: $regions,
        autoCapacityMarketTarget: $autoCapacityMarketTarget,
        tx: $tx,
    ) {
        tree_to_string(demand_tree, level=2)
    }
}}"""
