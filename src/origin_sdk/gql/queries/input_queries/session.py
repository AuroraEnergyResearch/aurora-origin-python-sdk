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
