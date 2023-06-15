from origin_sdk.gql.queries.input_queries import (
    create_get_session_gql,
)
from origin_sdk.gql.queries.input_queries.utils import (
    yearly_values_with_transform,
)
from origin_sdk.gql.queries.input_queries.utils import RecursiveTree, tree_to_string

commodities_document_fragment: RecursiveTree = {
    "commodity": None,
    "regions": None,
    "prices": yearly_values_with_transform,
}

get_commodities_gql = create_get_session_gql(
    {"regions": "[String]", "nativeUnitsFlag": "Boolean", "commodities": "[String!]"},
    {
        (
            """commodities (
    regions: $regions,
    commodities: $commodities,
    applyCommodityUnitConversionFactor: $nativeUnitsFlag
)"""
        ): commodities_document_fragment
    },
)

update_commodity_gql = f"""mutation (
    $sessionId: String!,
    $commodity: String!,
    $regions: [String!],
    $nativeUnitsFlag: Boolean,
    $tx: [YearlyNumberItemInput!]!
) {{
    updateCommodity (
        sessionId: $sessionId,
        regions: $regions,
        commodity: $commodity,
        tx: $tx,
        applyCommodityUnitConversionFactor: $nativeUnitsFlag,
    ) {
        tree_to_string(commodities_document_fragment)
    }
}}"""

rebase_commodities_gql = """mutation (
    $sessionId: String!,
    $rebaseReferenceId: String!,
    $rebaseReferenceType: EnumRebaseReferenceType
) {
    rebaseCommodities (
        sessionId: $sessionId,
        rebaseReferenceId: $rebaseReferenceId,
        rebaseReferenceType: $rebaseReferenceType
    ) {
        result
    }
}"""
