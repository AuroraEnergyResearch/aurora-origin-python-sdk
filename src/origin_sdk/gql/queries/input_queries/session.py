from typing import Dict
from origin_sdk.gql.queries.input_queries.utils import RecursiveTree, tree_to_string


def create_get_session_gql(variables: Dict[str, str], select: RecursiveTree):
    """Creates a getSession query, since this is the most common wrapper for
    queries.

    Arguments:
        variables: A dictionary of variables to be declared in the query
        select: The projection/query body to specify.
    """
    
    query: RecursiveTree = {
        "getSession (sessionId: $sessionId)": select,
    }
    
    return f'''query ( $sessionId: String!, {", ".join([f"""${
        key
    }: {
        value
    }""" for key, value in variables.items()])}) {
        tree_to_string(query)
    }'''


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
}

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
            "userPermissions": None,
        }
    }
)

get_session_information_gql = create_get_session_gql(
    {},
    {
        "meta": {"sessionId": None, "tenant": None},
        "dataGroups": None,
        "currencyInformation": None,
        "defaultCurrency": None,
        # "transforms": None,
        "productRegionInformation": {
            "code": None,
            "enabledRegions": {
                "code": None,
                "isFocusRegion": None,
                "isEndogenous": None,
                "isMainRegion": None,
                "hasCapacityMarket": None,
            },
        },
        "dataGroupEligibility": None,
    },
)
