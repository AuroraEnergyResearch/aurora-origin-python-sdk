from origin_sdk.gql.queries.input_queries.session import create_get_session_gql


get_technology_names_gql = create_get_session_gql(
    {"regions": "[String]"},
    {
        "technologyNames(regions: $regions)": None,
        "getTechnologyGroupings": None,
    },
)
