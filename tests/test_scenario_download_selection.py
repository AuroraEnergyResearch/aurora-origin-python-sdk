import pytest
from core.data import _get_scenario_output_cache_filename
from origin_sdk.service.Scenario import Scenario


def test_get_matching_download_definitions_filters_by_sub_type():
    data_definitions = [
        {"type": "technology", "granularity": "30M", "subType": "generation"},
        {
            "type": "technology",
            "granularity": "30M",
            "subType": "generation_pre_curtailment",
        },
    ]

    matches = Scenario._Scenario__get_matching_download_definitions(
        data_definitions,
        download_type="technology",
        granularity="30M",
        sub_type="generation_pre_curtailment",
    )

    assert len(matches) == 1
    assert matches[0].get("subType") == "generation_pre_curtailment"


def test_get_matching_download_definitions_without_sub_type_keeps_all_matches():
    data_definitions = [
        {"type": "technology", "granularity": "30M", "subType": "generation"},
        {
            "type": "technology",
            "granularity": "30M",
            "subType": "generation_pre_curtailment",
        },
        {"type": "system", "granularity": "30M"},
    ]

    matches = Scenario._Scenario__get_matching_download_definitions(
        data_definitions,
        download_type="technology",
        granularity="30M",
    )

    assert len(matches) == 2


def test_get_scenario_output_cache_filename_includes_sub_type_in_cache_key():
    without_sub_type = _get_scenario_output_cache_filename(
        region="gbr",
        download_type="technology",
        granularity="30M",
        currency="gbp2024",
        node=None,
        params={},
    )
    with_sub_type = _get_scenario_output_cache_filename(
        region="gbr",
        download_type="technology",
        granularity="30M",
        currency="gbp2024",
        node=None,
        params={},
        sub_type="generation_pre_curtailment",
    )

    assert without_sub_type != with_sub_type
    assert "-subtype-generation_pre_curtailment" in with_sub_type


class _FakeResponse:
    def __init__(self, status_code=200, headers=None, text=""):
        self.status_code = status_code
        self.headers = headers or {}
        self.text = text


class _FakeHttpClient:
    def __init__(self, responses=None):
        self.calls = []
        self.responses = list(responses or [])

    def request(self, method, url, params=None):
        self.calls.append({"method": method, "url": url, "params": params})
        if self.responses:
            return self.responses.pop(0)
        if len(self.calls) == 1:
            return _FakeResponse(headers={"location": "https://s3.local/mock.csv"})
        return _FakeResponse(text="header\nvalue")


class _FakeOriginSession:
    scenario_service_url = "https://origin.local"

    def __init__(self, session):
        self.session = session


def _build_test_scenario(meta_definitions, http_client):
    scenario = object.__new__(Scenario)
    scenario.scenario_id = "scenario-id"
    scenario.scenario = {"defaultCurrency": "gbp2024"}
    scenario.session = _FakeOriginSession(http_client)
    scenario.get_scenario_region = lambda region: {"dataUrlBase": "download/"}
    scenario.get_download_years = lambda region: [2028, 2029]
    scenario._Scenario__get_download_meta_for_region = lambda region: {
        "dataDefinitions": meta_definitions
    }
    return scenario


def test_get_scenario_data_csv_raises_clear_error_for_ambiguous_subtypes(monkeypatch):
    data_definitions = [
        {
            "type": "technology",
            "granularity": "30M",
            "subType": "generation",
            "filename": "technology_generation_{currency}.csv",
        },
        {
            "type": "technology",
            "granularity": "30M",
            "subType": "generation_pre_curtailment",
            "filename": "technology_generation_pre_curtailment_{currency}.csv",
        },
    ]

    scenario = _build_test_scenario(data_definitions, _FakeHttpClient())
    monkeypatch.setattr(
        "origin_sdk.service.Scenario.get_scenario_outputs_from_cache",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        "origin_sdk.service.Scenario.save_scenario_outputs_to_cache",
        lambda *args, **kwargs: None,
    )

    with pytest.raises(Exception) as err:
        scenario.get_scenario_data_csv(
            region="gbr",
            download_type="technology",
            granularity="30M",
            force_no_cache=True,
        )

    assert "pass sub_type to disambiguate" in str(err.value)


def test_get_scenario_data_csv_selects_requested_sub_type(monkeypatch):
    data_definitions = [
        {
            "type": "technology",
            "granularity": "30M",
            "subType": "generation",
            "filename": "technology_generation_{currency}.csv",
        },
        {
            "type": "technology",
            "granularity": "30M",
            "subType": "generation_pre_curtailment",
            "filename": "technology_generation_pre_curtailment_{currency}.csv",
        },
    ]

    http_client = _FakeHttpClient()
    scenario = _build_test_scenario(data_definitions, http_client)
    monkeypatch.setattr(
        "origin_sdk.service.Scenario.get_scenario_outputs_from_cache",
        lambda *args, **kwargs: None,
    )
    saved_sub_types = []

    def _capture_save(*args, **kwargs):
        saved_sub_types.append(kwargs.get("sub_type"))

    monkeypatch.setattr(
        "origin_sdk.service.Scenario.save_scenario_outputs_to_cache",
        _capture_save,
    )

    csv_data = scenario.get_scenario_data_csv(
        region="gbr",
        download_type="technology",
        granularity="30M",
        sub_type="generation_pre_curtailment",
        force_no_cache=True,
    )

    assert csv_data == "header\nvalue"
    assert saved_sub_types == ["generation_pre_curtailment"]
    assert (
        http_client.calls[0]["url"]
        == "https://origin.local/download/technology_generation_pre_curtailment_gbp2024.csv"
    )


def test_get_scenario_data_download_url_returns_signed_location():
    http_client = _FakeHttpClient()
    scenario = _build_test_scenario(
        [
            {
                "type": "system",
                "granularity": "1y",
                "filename": "system_{currency}.csv",
            }
        ],
        http_client,
    )

    result = scenario.get_scenario_data_download_url(
        region="gbr",
        download_type="system",
        granularity="1y",
        currency="gbp2024",
        params={"foo": "bar"},
    )

    assert result == "https://s3.local/mock.csv"
    assert http_client.calls == [
        {
            "method": "GET",
            "url": "https://origin.local/download/system_gbp2024.csv",
            "params": {"noredirect": "true", "checkstatus": "true", "foo": "bar"},
        }
    ]


def test_get_scenario_data_download_url_retries_while_file_generates(monkeypatch):
    http_client = _FakeHttpClient(
        [
            _FakeResponse(status_code=425),
            _FakeResponse(headers={"location": "https://s3.local/mock.csv"}),
        ]
    )
    scenario = _build_test_scenario(
        [
            {
                "type": "system",
                "granularity": "1y",
                "filename": "system_{currency}.csv",
            }
        ],
        http_client,
    )
    monkeypatch.setattr("origin_sdk.service.Scenario.sleep", lambda seconds: None)

    result = scenario.get_scenario_data_download_url("gbr", "system", "1y")

    assert result == "https://s3.local/mock.csv"
    assert len(http_client.calls) == 2


def test_get_scenario_data_download_url_validates_required_node():
    scenario = _build_test_scenario(
        [
            {
                "type": "nodal",
                "granularity": "1h",
                "filename": "nodal_{nodename}.csv",
            }
        ],
        _FakeHttpClient(),
    )

    with pytest.raises(Exception, match="requires node parameter"):
        scenario.get_scenario_data_download_url("gbr", "nodal", "1h")


def test_get_scenario_data_download_url_validates_unsupported_year():
    scenario = _build_test_scenario(
        [
            {
                "type": "system",
                "granularity": "1y",
                "filename": "system_{currency}.csv",
            }
        ],
        _FakeHttpClient(),
    )

    with pytest.raises(Exception, match="does not support year parameter"):
        scenario.get_scenario_data_download_url("gbr", "system", "1y", year=2030)


def test_get_scenario_data_download_url_errors_when_location_missing():
    http_client = _FakeHttpClient([_FakeResponse()])
    scenario = _build_test_scenario(
        [
            {
                "type": "system",
                "granularity": "1y",
                "filename": "system_{currency}.csv",
            }
        ],
        http_client,
    )

    with pytest.raises(Exception, match="Could not get download location"):
        scenario.get_scenario_data_download_url("gbr", "system", "1y")


def test_get_scenario_data_csv_returns_cached_value_without_request(monkeypatch):
    http_client = _FakeHttpClient()
    scenario = _build_test_scenario(
        [
            {
                "type": "system",
                "granularity": "1y",
                "filename": "system_{currency}.csv",
            }
        ],
        http_client,
    )

    monkeypatch.setattr(
        "origin_sdk.service.Scenario.get_scenario_outputs_from_cache",
        lambda *args, **kwargs: "cached,csv\n",
    )

    result = scenario.get_scenario_data_csv("gbr", "system", "1y")

    assert result == "cached,csv\n"
    assert http_client.calls == []
