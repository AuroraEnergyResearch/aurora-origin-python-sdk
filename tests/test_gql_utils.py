from origin_sdk.gql.queries.input_queries.session import (
    create_get_session_gql,
    tree_to_string,
    RecursiveTree,
)

test_object: RecursiveTree = {
    "a": None,
    "b": None,
    "c": "ShouldNotTree",
    "d": ["Could", "Tree", "But", "shouldn't"],
    "e": {"Will": True, "For": True, "Sure": True, "Tree": False},
    "getTechnology (technologyName: $technologyName)": {"name": None},
}


def test_tree_to_string_works(snapshot):
    stringed_tree = tree_to_string(test_object)
    snapshot.assert_match(stringed_tree, "should_look_like_a_nice_gql_query.txt")


def test_create_get_session_gql_func(snapshot):
    query = create_get_session_gql({"technologyName": "String!"}, test_object)
    snapshot.assert_match(query, "same_as_other_one_wrapped_in_get_session.txt")


def test_more_realistic_create_get_session_gql_example(snapshot):
    query = create_get_session_gql(
        {"regions": "[String]"},
        {
            "technologyNames(regions: $regions)": None,
            "getTechnologyGroupings": None,
        },
    )
    snapshot.assert_match(query, "get_technology_names_query.txt")
