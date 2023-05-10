from typing import Dict
from origin_sdk.gql.queries.input_queries.utils import RecursiveTree, tree_to_string


def create_get_session_gql(variables: Dict[str, str], select: RecursiveTree):
    query: RecursiveTree = {"getSession (sessionId: $sessionId)": select}
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
        "sessionId": None,
        "dataGroups": None,
        "currencyInformation": None,
        "defaultCurrency": None,
        "transforms": None,
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
