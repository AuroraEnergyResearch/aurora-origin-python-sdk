from __future__ import annotations

from types import SimpleNamespace

import pytest

from origin_sdk.service import Scenario as scenario_module
from origin_sdk.service.Scenario import Scenario


class FakeResponse:
    def __init__(self, *, location: str | None = None, text: str = "") -> None:
        self.headers = {}
        if location is not None:
            self.headers["location"] = location
        self.status_code = 200
        self.text = text


class FakeHttpSession:
    def __init__(self) -> None:
        self.requests: list[tuple[str, str, dict[str, str] | None]] = []
        self.responses: list[FakeResponse] = []

    def request(
        self, method: str, url: str, params: dict[str, str] | None = None
    ) -> FakeResponse:
        self.requests.append((method, url, params))
        return self.responses.pop(0)


def test_get_scenario_data_download_url_returns_signed_location() -> None:
    http = FakeHttpSession()
    http.responses.append(FakeResponse(location="https://signed.example/file.csv"))
    scenario = _scenario(http)

    result = scenario.get_scenario_data_download_url(
        region="gbr",
        download_type="system",
        granularity="1y",
        currency="gbp2024",
        params={"foo": "bar"},
    )

    assert result == "https://signed.example/file.csv"
    assert http.requests == [
        (
            "GET",
            "https://scenario.example/outputs/gbr/system_gbp2024.csv",
            {"noredirect": "true", "checkstatus": "true", "foo": "bar"},
        )
    ]


def test_get_scenario_data_download_url_retries_while_file_generates(
    monkeypatch,
) -> None:
    http = FakeHttpSession()
    first_response = FakeResponse()
    first_response.status_code = 425
    http.responses.extend(
        [first_response, FakeResponse(location="https://signed.example/file.csv")]
    )
    scenario = _scenario(http)
    monkeypatch.setattr(scenario_module, "sleep", lambda seconds: None)

    result = scenario.get_scenario_data_download_url(
        region="gbr",
        download_type="system",
        granularity="1y",
    )

    assert result == "https://signed.example/file.csv"
    assert len(http.requests) == 2


def test_get_scenario_data_download_url_validates_required_node() -> None:
    scenario = _scenario(FakeHttpSession(), filename="nodal_{nodename}.csv")

    with pytest.raises(Exception, match="requires node parameter"):
        scenario.get_scenario_data_download_url(
            region="gbr",
            download_type="nodal",
            granularity="1h",
        )


def test_get_scenario_data_download_url_validates_unsupported_year() -> None:
    scenario = _scenario(FakeHttpSession())

    with pytest.raises(Exception, match="does not support year parameter"):
        scenario.get_scenario_data_download_url(
            region="gbr",
            download_type="system",
            granularity="1y",
            year=2030,
        )


def test_get_scenario_data_download_url_errors_when_location_missing() -> None:
    http = FakeHttpSession()
    http.responses.append(FakeResponse())
    scenario = _scenario(http)

    with pytest.raises(Exception, match="Could not get download location"):
        scenario.get_scenario_data_download_url(
            region="gbr",
            download_type="system",
            granularity="1y",
        )


def test_get_scenario_data_csv_uses_download_url_and_preserves_cache(
    monkeypatch,
) -> None:
    http = FakeHttpSession()
    http.responses.extend(
        [
            FakeResponse(location="https://signed.example/file.csv"),
            FakeResponse(text="a,b\n1,2\n"),
        ]
    )
    scenario = _scenario(http)
    saved: dict[str, object] = {}

    monkeypatch.setattr(
        scenario_module, "get_scenario_outputs_from_cache", lambda *args, **kwargs: None
    )

    def save_cache(*args, **kwargs):
        saved["args"] = args
        saved["kwargs"] = kwargs

    monkeypatch.setattr(scenario_module, "save_scenario_outputs_to_cache", save_cache)

    result = scenario.get_scenario_data_csv("gbr", "system", "1y")

    assert result == "a,b\n1,2\n"
    assert http.requests[-1] == ("GET", "https://signed.example/file.csv", None)
    assert saved["args"][:9] == (
        "scenario-1",
        "gbr",
        "system",
        "1y",
        "gbp2024",
        None,
        None,
        "a,b\n1,2\n",
        {},
    )
    assert saved["kwargs"] == {"sub_type": None}


def test_get_scenario_data_csv_returns_cached_value_without_request(
    monkeypatch,
) -> None:
    http = FakeHttpSession()
    scenario = _scenario(http)

    monkeypatch.setattr(
        scenario_module,
        "get_scenario_outputs_from_cache",
        lambda *args, **kwargs: "cached,csv\n",
    )

    result = scenario.get_scenario_data_csv("gbr", "system", "1y")

    assert result == "cached,csv\n"
    assert http.requests == []


def _scenario(
    http: FakeHttpSession, filename: str = "system_{currency}.csv"
) -> Scenario:
    scenario = Scenario.__new__(Scenario)
    scenario.scenario_id = "scenario-1"
    scenario.scenario = {"defaultCurrency": "gbp2024"}
    scenario.session = SimpleNamespace(
        scenario_service_url="https://scenario.example",
        session=http,
    )
    scenario.get_scenario_region = lambda region: {"dataUrlBase": f"outputs/{region}/"}  # type: ignore[method-assign]
    scenario.get_download_years = lambda region: [2028, 2029]  # type: ignore[method-assign]
    scenario._Scenario__get_download_meta_for_region = lambda region: {  # type: ignore[attr-defined]
        "dataDefinitions": [
            {
                "type": "system" if "nodal" not in filename else "nodal",
                "granularity": "1y" if "nodal" not in filename else "1h",
                "filename": filename,
            }
        ]
    }
    return scenario
