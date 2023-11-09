from typing import Any
from origin_sdk.gql.queries.input_queries.utils import RecursiveTree, tree_to_string


config_tech_params_subtree = {
    "name": None,
    "type": None,
    "units": None,
    "lock": None,
    "aggregationMethod": None,
    "appliesToEndoBui": None,
    "appliesToExo": None,
    "loadFactorTechRequired": None,
    "thermalTechRequired": None,
    "initialRange": {
        "upper": None,
        "lower": None,
    },
    "hardLimit": {
        "upper": None,
        "lower": None,
    },
    "isMonthlyRegionTechParameter": None,
}

demand_var_subtree: RecursiveTree = {"name": None, "type": None, "units": None}


get_config_gql = tree_to_string(
    {
        "getConfig": {
            "technology": {
                "definitions": {
                    "name": None,
                    "isLoadFactor": None,
                    "isThermal": None,
                    "readOnlyParameters": None,
                },
                "parameters": config_tech_params_subtree,
                "definitionParameters": config_tech_params_subtree,
            },
            "demand": {
                "demandVariables": demand_var_subtree,
                "demandTechnologyVariables": demand_var_subtree,
            },
            "userPermissions": None,
            "commodities": {
                "regionMapping": None,
                "commoditiesAvailable": {"units": None, "name": None},
            },
        }
    }
)


def get_endo_exo_param_list_from_config(tech_config: Any):
    pd = tech_config.get("definitionParameters")
    ppy = tech_config.get("parameters")
    exo_params_yearly = [
        param.get("name")
        for param in ppy
        if param.get("appliesToExo") is True
        and param.get("isMonthlyRegionTechParameter") is False
    ]
    exo_params_monthly = [
        param.get("name")
        for param in ppy
        if param.get("appliesToExo") is True
        and param.get("isMonthlyRegionTechParameter") is True
    ]
    endo_params_yearly = [
        param.get("name")
        for param in ppy
        if param.get("appliesToEndoBui") is True
        and param.get("isMonthlyRegionTechParameter") is False
    ]
    endo_params_monthly = [
        param.get("name")
        for param in ppy
        if param.get("appliesToEndoBui") is True
        and param.get("isMonthlyRegionTechParameter") is True
    ]
    exo_defs = [param.get("name") for param in pd if param.get("appliesToExo") is True]
    endo_defs = [
        param.get("name") for param in pd if param.get("appliesToEndoBui") is True
    ]

    return (
        exo_params_yearly,
        exo_params_monthly,
        endo_params_yearly,
        endo_params_monthly,
        exo_defs,
        endo_defs,
    )


def get_demand_variables_from_config(demand_config: Any):
    system = [var.get("name") for var in demand_config.get("demandVariables")]
    tech = [var.get("name") for var in demand_config.get("demandTechnologyVariables")]

    return (system, tech)
