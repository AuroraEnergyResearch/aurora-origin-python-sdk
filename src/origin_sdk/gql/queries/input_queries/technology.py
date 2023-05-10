from origin_sdk.gql.queries.input_queries.session import (
    create_get_session_gql,
    yearly_values_with_transform,
    variable_values,
)
from origin_sdk.gql.queries.input_queries.utils import RecursiveTree, tree_to_string


get_technology_names_gql = create_get_session_gql(
    {"regions": "[String]"},
    {
        "technologyNames(regions: $regions)": None,
        "getTechnologyGroupings": None,
    },
)

plant_parameters_fragment: RecursiveTree = {
    "parameters": {
        key: yearly_values_with_transform
        for key in [
            "capacity",
            "capex",
            "opex",
            "lifetimeBuildLimit",
            "yearlyBuildLimit",
            "loadFactorAverage",
            "efficiency",
            "efficiencySEL",
            "marginalLossFactor",
        ]
    }
}

plant_definitions_fragment = {
    "definitions": {key: variable_values for key in ["discountRate", "discountRateLow"]}
}

tech_original_fragment = {"technology": {"original": None}}

aggregated_plants_fragment: RecursiveTree = {
    "exogenous": {**tech_original_fragment, **plant_parameters_fragment},
    "endogenous": {
        **tech_original_fragment,
        **plant_parameters_fragment,
        **plant_definitions_fragment,
    },
}

get_technology_gql = create_get_session_gql(
    {"technologyName": "String!", "regions": "[String!]"},
    {
        (
            "baseTechnology ( technology: $technologyName, regions: $regions ) "
        ): aggregated_plants_fragment
    },
)

update_technology_gql = f"""mutation(
    $sessionId: String!,
    $techName: String!,
    $parameter: PlantParameter!,
    $endoExo: EnumEndoExo!,
    $tx: [OptionalYearlyNumberItemInput!]!,
    $regions: [String!]
) {{
    updateTechnologyParameter(
        sessionId: $sessionId,
        technology: $techName,
        parameter: $parameter,
        endoExo: $endoExo,
        tx: $tx,
        regions: $regions
    ) {tree_to_string(aggregated_plants_fragment)}
}}"""
