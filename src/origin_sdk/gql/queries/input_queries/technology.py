from typing import Any, List, Optional
from origin_sdk.gql.queries.input_queries import (
    create_get_session_gql,
)
from origin_sdk.gql.queries.input_queries.utils import (
    yearly_values_with_transform,
    variable_values_with_transform,
    variable_values,
)
from origin_sdk.gql.queries.input_queries.utils import RecursiveTree, tree_to_string


get_technology_names_gql = create_get_session_gql(
    {},
    {
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


def get_endo_exo_param_list_from_config(tech_config: Any):
    pd = tech_config.get("definitionParameters")
    ppy = tech_config.get("parameters")
    exo_params = [
        param.get("name") for param in ppy if param.get("appliesToExo") is True
    ]
    endo_params = [
        param.get("name") for param in ppy if param.get("appliesToEndoBui") is True
    ]
    exo_defs = [param.get("name") for param in pd if param.get("appliesToExo") is True]
    endo_defs = [
        param.get("name") for param in pd if param.get("appliesToEndoBui") is True
    ]

    return (exo_params, endo_params, exo_defs, endo_defs)


def get_endo_param_and_def_tree(
    endo_params: Optional[List[str]] = None, endo_defs: Optional[List[str]] = None
):
    return {
        **(
            {
                "parameters": {
                    param: yearly_values_with_transform for param in endo_params
                }
            }
            if endo_params is not None
            else {}
        ),
        **(
            {
                "definitions": {
                    param: variable_values_with_transform for param in endo_defs
                }
            }
            if endo_defs is not None
            else {}
        ),
    }


def get_exo_param_and_def_tree(
    exo_params: Optional[List[str]] = None, exo_defs: Optional[List[str]] = None
):
    return {
        **(
            {
                "parameters": {
                    param: yearly_values_with_transform for param in exo_params
                }
            }
            if exo_params is not None
            else {}
        ),
        **(
            {
                "definitions": {
                    param: variable_values_with_transform for param in exo_defs
                }
            }
            if exo_defs is not None
            else {}
        ),
    }


def get_technology_gql(tech_config: Any):
    exo_params, endo_params, exo_defs, endo_defs = get_endo_exo_param_list_from_config(
        tech_config
    )
    exo_tree = get_exo_param_and_def_tree(exo_params=exo_params)
    endo_tree = get_endo_param_and_def_tree(
        endo_params=endo_params, endo_defs=endo_defs
    )
    return create_get_session_gql(
        {
            "techName": "String!",
            "region": "String!",
            "subregion": "String",
            "exoSubTechnology": "String",
            "subsidy": "String",
            "endoSubTechnology": "String",
        },
        {
            (
                "getTechnology ( name: $techName, region: $region, subRegion: $subregion ) "
            ): {
                "name": None,
                "region": None,
                "isRenewable": None,
                "technologyGrouping": None,
                "getExogenous( subTechnology: $exoSubTechnology, subsidy: $subsidy)": exo_tree,
                "getEndogenous( subTechnology: $endoSubTechnology )": endo_tree,
            }
        },
    )


def update_endo_technology_gql(tech_config: Any):
    _, endo_params, _, endo_defs = get_endo_exo_param_list_from_config(tech_config)
    return f"""mutation (
    $sessionId: String!,
    $parameter: EndogenousPlantVariable!,
    $tx: [OptionalYearlyNumberItemInput!]!,
    $name: String!,
    $region: String!
    $subRegion: String,
    $subTechnology: String ) {{
        updateEndogenousTechnologyParameter(
            sessionId: $sessionId,
            parameter: $parameter,
            tx: $tx,
            name: $name,
            region: $region,
            subRegion: $subRegion,
            subTechnology: $subTechnology) {
                tree_to_string(
                    get_endo_param_and_def_tree(
                        endo_params,
                        endo_defs
                    )
                )
            }
    }}
    """


def update_exo_technology_gql(tech_config: Any):
    exo_params, _, _, _ = get_endo_exo_param_list_from_config(tech_config)
    return f"""mutation (
    $sessionId: String!,
    $parameter: ExogenousPlantVariable!,
    $tx: [OptionalYearlyNumberItemInput!]!,
    $name: String!,
    $region: String!
    $subRegion: String,
    $subsidy: String,
    $subTechnology: String) {{
        updateExogenousTechnologyParameter(
            sessionId: $sessionId,
            parameter: $parameter,
            tx: $tx,
            name: $name,
            region: $region,
            subRegion: $subRegion,
            subsidy: $subsidy,
            subTechnology: $subTechnology) {
                tree_to_string(
                    get_exo_param_and_def_tree(
                        exo_params
                    )
                )
            }
    }}
    """
