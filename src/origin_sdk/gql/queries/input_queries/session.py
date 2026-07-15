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
        "modelMaxYear": None,
        "modelMinYear": None,
        "transforms": {"updateParameters": None, "steps": None, "reason": None},
    },
)
