from origin_sdk.gql.fragments.scenario import scenario_summary_fields

get_origin_dash_config = """
query {
  getConfig {
    regionGroups
    currencies
    sensitivities
    products
    isAuthor
    isAdvancedUser
    appsSupported
  }
}
"""


def build_get_projects(limit=False, offset=False, name=False):
    """Build the getProjects query.

    Pagination variables are only declared/forwarded when the caller actually
    supplies them. When none are supplied the query is identical to the
    original, so it remains compatible with backends that predate pagination
    support.
    """
    declarations = []
    arguments = []
    if limit:
        declarations.append("$limit: Int")
        arguments.append("limit: $limit")
    if offset:
        declarations.append("$offset: Int")
        arguments.append("offset: $offset")
    if name:
        declarations.append("$name: String")
        arguments.append("name: $name")

    declaration_str = f" ({', '.join(declarations)})" if declarations else ""
    argument_str = f" ({', '.join(arguments)})" if arguments else ""

    return f"""
query{declaration_str} {{
  getProjects{argument_str} {{
    projectGlobalId
    name
    description
    isProjectPinned
  }}
}}
"""


def build_get_project(scenario_limit=False, scenario_offset=False):
    """Build the getProject query.

    Nested-scenario pagination args are only declared/forwarded when supplied,
    keeping the default query compatible with backends that predate pagination
    support.
    """
    declarations = ["$projectId: String!"]
    scenario_arguments = []
    if scenario_limit:
        declarations.append("$scenarioLimit: Int")
        scenario_arguments.append("limit: $scenarioLimit")
    if scenario_offset:
        declarations.append("$scenarioOffset: Int")
        scenario_arguments.append("offset: $scenarioOffset")

    scenario_argument_str = (
        f" ({', '.join(scenario_arguments)})" if scenario_arguments else ""
    )

    return f"""
query ({', '.join(declarations)}) {{
  getProject (projectGlobalId: $projectId) {{
    projectGlobalId
    name
    description
    productName
    productId
    isProjectPinned
    scenarios{scenario_argument_str} {{
      {scenario_summary_fields}
    }}
  }}
}}
"""


create_project = """
mutation ($project: InputProject!) {
  createProject (project: $project) {
    projectGlobalId
    name
    description
    productId
  }
}
"""

update_project = """
mutation ($project: UpdateProjectInputGroup!) {
  updateProject (project: $project) {
    projectGlobalId
    name
    description
    productId
    isProjectPinned
  }
}
"""

delete_project = """
mutation ($projectGlobalId: String!) {
  deleteProject (projectGlobalId: $projectGlobalId)
}
"""

pin_project = """
mutation ($projectGlobalId: String!) {
  createProjectPin (projectGlobalId: $projectGlobalId)
}
"""

unpin_project = """
mutation ($projectGlobalId: String!) {
  deleteProjectPin (projectGlobalId: $projectGlobalId)
}
"""
