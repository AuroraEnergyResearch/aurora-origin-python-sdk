"""Unit tests for the pagination arguments on the listing endpoints.

These do not hit the network: ``_graphql_request`` is patched to capture the
GraphQL variables that the session would send.
"""

from unittest.mock import patch

from origin_sdk.OriginSession import OriginSession


def _query_and_variables_for(call):
    # _graphql_request is called as (url, query, variables) because
    # patch.object replaces the attribute (self is not re-bound).
    args, kwargs = call
    query = kwargs.get("query", args[1] if len(args) > 1 else None)
    variables = kwargs.get("variables", args[2] if len(args) > 2 else None)
    return query, variables


def _capture(method_name, *args, **kwargs):
    session = OriginSession({"token": "test-token"})
    with patch.object(
        OriginSession, "_graphql_request", return_value=[]
    ) as mock_request:
        getattr(session, method_name)(*args, **kwargs)
    return _query_and_variables_for(mock_request.call_args)


def _call_capturing(method_name, *args, **kwargs):
    _query, variables = _capture(method_name, *args, **kwargs)
    return variables


def test_get_projects_omits_pagination_when_not_supplied():
    assert _call_capturing("get_projects") == {}


def test_get_projects_includes_supplied_pagination():
    assert _call_capturing("get_projects", limit=10, offset=20, name="GB") == {
        "limit": 10,
        "offset": 20,
        "name": "GB",
    }


def test_get_projects_includes_only_supplied_fields():
    assert _call_capturing("get_projects", name="GB") == {"name": "GB"}


def test_get_project_forwards_scenario_pagination():
    assert _call_capturing(
        "get_project", "project-id", scenario_limit=5, scenario_offset=2
    ) == {
        "projectId": "project-id",
        "scenarioLimit": 5,
        "scenarioOffset": 2,
    }


def test_get_project_without_pagination_only_sends_id():
    assert _call_capturing("get_project", "project-id") == {"projectId": "project-id"}


def test_get_aurora_scenarios_includes_pagination_in_filter():
    assert _call_capturing(
        "get_aurora_scenarios", region="GBR", limit=5, offset=10
    ) == {
        "filter": {
            "regionGroupCode": "GBR",
            "limit": 5,
            "offset": 10,
            "scenarioType": "AURORA_SCENARIO",
        }
    }


def test_get_aurora_scenarios_without_pagination_unchanged():
    assert _call_capturing("get_aurora_scenarios", region="GBR") == {
        "filter": {
            "regionGroupCode": "GBR",
            "scenarioType": "AURORA_SCENARIO",
        }
    }


# --- Backward compatibility: a no-pagination call must not reference the new
# pagination arguments in the query text, so it stays valid against backends
# that predate pagination support. ---


def test_get_projects_query_omits_pagination_args_by_default():
    query, _ = _capture("get_projects")
    assert "limit" not in query
    assert "offset" not in query
    assert "name: $name" not in query


def test_get_projects_query_includes_requested_pagination_args():
    query, _ = _capture("get_projects", limit=5)
    assert "$limit: Int" in query
    assert "limit: $limit" in query
    assert "offset" not in query


def test_get_project_query_omits_scenario_pagination_by_default():
    query, _ = _capture("get_project", "project-id")
    assert "scenarioLimit" not in query
    assert "scenarioOffset" not in query
    assert "scenarios {" in query


def test_get_project_query_includes_requested_scenario_pagination():
    query, _ = _capture("get_project", "project-id", scenario_limit=10)
    assert "$scenarioLimit: Int" in query
    assert "limit: $scenarioLimit" in query
