from origin_sdk.gql.fragments.scenario import scenario_summary_fields

get_origin_regions = """
query {
  getConfig {
    regionGroups
  }
}
"""

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

get_projects = """
query {
  getProjects {
    projectGlobalId
    name
    description
    isProjectPinned
  }
}
"""

get_project = f"""
query ($projectId: String!) {{
  getProject (projectGlobalId: $projectId) {{
    projectGlobalId
    name
    description
    productName
    productId
    isProjectPinned
    scenarios {{
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
