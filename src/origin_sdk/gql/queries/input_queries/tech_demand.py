from typing import Any, List
from origin_sdk.gql.queries.input_queries.config import get_demand_variables_from_config
from origin_sdk.gql.queries.input_queries.session import create_get_session_gql
from origin_sdk.gql.queries.input_queries.utils import (
    RecursiveTree,
    tree_to_string,
    variable_values_with_transform,
    original_value_only,
)


def create_demand_tech_tree(tech_vars: List[str]) -> RecursiveTree:
    return {
        **{
            key: original_value_only
            for key in ["region", "technology", "originTechnology"]
        },
        "variables": {
            "year": None,
            **{variable: variable_values_with_transform for variable in tech_vars},
        },
    }


def get_demand_technology_names():
    return create_get_session_gql(
        {"demTechFilter": "GetDemandTechFilterDemandTechnologyInput"},
        {
            "getDemandTechnologies (filter: $demTechFilter)": {
                "region": None,
                "originTechnology": None,
            }
        },
    )


def get_demand_technologies_gql(demand_config: Any):
    _, tech = get_demand_variables_from_config(demand_config)
    return create_get_session_gql(
        {"demTechFilter": "GetDemandTechFilterDemandTechnologyInput"},
        {
            "getDemandTechnologies (filter: $demTechFilter)": create_demand_tech_tree(
                tech
            )
        },
    )


def update_demand_technology(demand_config: Any):
    _, tech = get_demand_variables_from_config(demand_config)
    return f"""mutation(
    $sessionId: String!,
    $technology: String!,
    $region: String!,
    $variable: EnumDemandTechnologyVariable!
    $autoCapacityMarketTarget: Boolean,
    $tx: [YearlyNumberItemInput!]!,
) {{
    updateDemandTechnologyVariable (
        sessionId: $sessionId,
        region: $region,
        technology: $technology,
        variable: $variable,
        autoCapacityMarketTarget: $autoCapacityMarketTarget,
        tx: $tx
    ) {tree_to_string(create_demand_tech_tree(tech), level=2)}
}}"""
