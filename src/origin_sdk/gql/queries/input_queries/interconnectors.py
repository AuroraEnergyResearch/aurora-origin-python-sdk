from typing import Any, List
from origin_sdk.gql.queries.input_queries.config import (
    get_interconnector_variables_from_config,
)
from origin_sdk.gql.queries.input_queries import create_get_session_gql
from origin_sdk.gql.queries.input_queries.utils import (
    RecursiveTree,
    variable_values_with_transform,
    tree_to_string,
)


def create_interconnector_tree(variables: List[str]) -> RecursiveTree:
    return {
        "ends": None,
        "from": None,
        "to": None,
        "asymmetric": {"original": None},
        "variables": {
            "year": None,
            **{variable: variable_values_with_transform for variable in variables},
        },
    }


def create_interconnector_end_tree() -> RecursiveTree:
    return {
        "ends": None,
    }


def get_interconnectors_gql(interconnector_config: Any):
    return create_get_session_gql(
        {"interconnectorFilter": "GetInterconnectorsFilterInterconnectorInput"},
        {
            "getInterconnectors (filter: $interconnectorFilter)": create_interconnector_tree(
                get_interconnector_variables_from_config(interconnector_config)
            )
        },
    )


def get_interconnectors_regions_gql():
    return create_get_session_gql(
        {"interconnectorFilter": "GetInterconnectorsFilterInterconnectorInput"},
        {
            "getInterconnectors (filter: $interconnectorFilter)": create_interconnector_end_tree()
        },
    )


def update_interconnectors(interconnector_config: Any):
    interconnector_tree = create_interconnector_tree(
        get_interconnector_variables_from_config(interconnector_config)
    )

    return f"""mutation (
    $sessionId: String!,
    $from: String!,
    $to: String!,
    $variable: String!,
    $tx: [YearlyNumberItemInput]!
) {{
    updateInterconnectorVariable (
        sessionId: $sessionId,
        from: $from,
        to: $to,
        variable: $variable,
        tx: $tx,
    ) {
        tree_to_string(interconnector_tree, level=2)
    }
}}"""
