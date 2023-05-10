from typing import Any
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


def get_technology_gql(tech_config: Any):
    pd = tech_config.get("definitionParameters")
    ppy = tech_config.get("parameters")
    exoParams = [
        param.get("name") for param in ppy if param.get("appliesToExo") is True
    ]
    endoParams = [
        param.get("name") for param in ppy if param.get("appliesToEndoBui") is True
    ]
    # exoDefs = [param.get("name") for param in pd if param.get("appliesToExo") is True]
    endoDefs = [
        param.get("name") for param in pd if param.get("appliesToEndoBui") is True
    ]
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
                "getExogenous( subTechnology: $exoSubTechnology, subsidy: $subsidy)": {
                    **(
                        {
                            "parameters": {
                                param: yearly_values_with_transform
                                for param in exoParams
                            }
                        }
                        if exoParams is not None
                        else {}
                    )
                },
                "getEndogenous( subTechnology: $endoSubTechnology )": {
                    **(
                        {
                            "parameters": {
                                param: yearly_values_with_transform
                                for param in endoParams
                            }
                        }
                        if endoParams is not None
                        else {}
                    ),
                    **(
                        {
                            "definitions": {
                                param: variable_values_with_transform
                                for param in endoDefs
                            }
                        }
                        if endoDefs is not None
                        else {}
                    ),
                },
            }
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
