import pytest
from origin_sdk.OriginSession import OriginSession
from origin_sdk.service.Scenario import Scenario, _validate_year_parameter

session = OriginSession()

test_scenario = None


def get_scenario_for_testing(region="gbr"):
    global test_scenario
    if test_scenario is None:
        test_scenario = Scenario.get_latest_scenario_from_region(
            session=session, region=region, name_filter="central"
        )

    return test_scenario


def test_construct_latest_gbr_scenario():
    scenario = get_scenario_for_testing()
    # The constructor passed, we are good to go, check the id exists
    assert scenario.scenario.get("scenarioGlobalId") is not None


def test_getting_latest_net_zero_scenario():
    test_scenario = Scenario.get_latest_scenario_from_region(
        session=session, region="gbr", name_filter="net zero"
    )

    # This function should be case insensitive
    test_scenario_caps = Scenario.get_latest_scenario_from_region(
        session=session, region="gbr", name_filter="NET ZERO"
    )

    assert test_scenario is not None
    assert test_scenario_caps is not None
    assert test_scenario.scenario_id == test_scenario_caps.scenario_id


def test_getting_central_apr_2022():
    test_scenario = Scenario.get_latest_scenario_from_region(
        session=session, region="gbr", name_filter=["central", "apr", "2022"]
    )

    # This function should be case insensitive
    test_scenario_caps = Scenario.get_latest_scenario_from_region(
        session=session, region="gbr", name_filter=["CENTRAL", "APR", "2022"]
    )

    assert test_scenario is not None
    assert test_scenario_caps is not None
    assert test_scenario.scenario_id == test_scenario_caps.scenario_id


def test_getting_a_silly_scenario_name_fails():
    try:
        Scenario.get_latest_scenario_from_region(
            session=session, region="gbr", name_filter="ZZZZZZZZZZZZXXXXXXXXXX"
        )
        assert False
    except Exception as e:
        assert "Scenario not found" in str(e)


def test_getting_a_silly_region_fails():
    try:
        Scenario.get_latest_scenario_from_region(session=session, region="NO_REGION")
        assert False
    except Exception as e:
        assert "Scenario not found" in str(e)


def test_downloadable_regions_function():
    scenario = get_scenario_for_testing()
    regions = scenario.get_downloadable_regions()
    assert isinstance(regions, list)
    assert len(regions) > 0


def test_get_scenario_region_function():
    scenario = get_scenario_for_testing()
    regions = scenario.get_downloadable_regions()
    all_info = [scenario.get_scenario_region(region) for region in regions]
    assert len([info for info in all_info if info is not None]) > 0


# TEST:
def test_get_download_types():
    scenario = get_scenario_for_testing()
    regions = scenario.get_downloadable_regions()
    download_types = {region: scenario.get_download_types(region) for region in regions}
    assert len(download_types) == len(regions)


@pytest.mark.skip("Method is deprecated now.")
def test_get_data_dfs():
    scenario = get_scenario_for_testing()
    regions = scenario.get_downloadable_regions()
    download_types = {region: scenario.get_download_types(region) for region in regions}

    yearly_dfs = [
        scenario.get_scenario_dataframe(
            region,
            type_granularity_combo.get("type"),
            type_granularity_combo.get("granularity"),
            force_no_cache=True,
        )
        for region in regions
        for type_granularity_combo in (download_types.get(region) or [])
        if type_granularity_combo.get("granularity") == "1y"
    ]

    assert all([df is not None for df in yearly_dfs])


# TEST:
def test_get_data_csvs():
    scenario = get_scenario_for_testing()
    regions = scenario.get_downloadable_regions()
    download_types = {region: scenario.get_download_types(region) for region in regions}

    yearly_csvs = [
        scenario.get_scenario_data_csv(
            region,
            type_granularity_combo.get("type"),
            type_granularity_combo.get("granularity"),
            force_no_cache=True,
        )
        for region in regions
        for type_granularity_combo in (download_types.get(region) or [])
        if type_granularity_combo.get("granularity") == "1y"
    ]

    assert all([len(csv) > 0 for csv in yearly_csvs])


def test_get_download_years():
    # set up
    aus_scenario = get_scenario_for_testing(region="aus")
    regions = aus_scenario.get_downloadable_regions()
    for region in regions:
        # function call we are testing
        years = aus_scenario.get_download_years(region)
        assert isinstance(years, list)
        assert isinstance(years[0], int)


def test_validate_year_raises_when_year_required_but_not_provided():
    try:
        _validate_year_parameter(
            year=None,
            year_supported=True,
            valid_years=[2028, 2029],
            download_type="interconnector",
            granularity="1h",
            region="peu_deu",
        )
        assert False
    except Exception as e:
        assert "requires year parameter" in str(e)
        assert "[2028, 2029]" in str(e)


def test_validate_year_raises_when_year_provided_but_not_supported():
    try:
        _validate_year_parameter(
            year=2028,
            year_supported=False,
            valid_years=[],
            download_type="system",
            granularity="1y",
            region="peu_deu",
        )
        assert False
    except Exception as e:
        assert "does not support year parameter" in str(e)


def test_validate_year_raises_when_year_not_in_valid_years():
    try:
        _validate_year_parameter(
            year=2030,
            year_supported=True,
            valid_years=[2028, 2029],
            download_type="interconnector",
            granularity="1h",
            region="peu_deu",
        )
        assert False
    except Exception as e:
        assert "not valid for region" in str(e)
        assert "[2028, 2029]" in str(e)


def test_validate_year_passes_when_year_valid():
    _validate_year_parameter(
        year=2028,
        year_supported=True,
        valid_years=[2028, 2029],
        download_type="interconnector",
        granularity="1h",
        region="peu_deu",
    )


def test_validate_year_passes_when_no_year_and_not_supported():
    _validate_year_parameter(
        year=None,
        year_supported=False,
        valid_years=[],
        download_type="system",
        granularity="1y",
        region="peu_deu",
    )


def test_refresh():
    scenario = get_scenario_for_testing()
    scenario.refresh()

    assert True


def test_get_shortcut():
    scenario = get_scenario_for_testing()
    scenario_keys = scenario.scenario.keys()
    all_keys_equal = all(
        [scenario.get(key) == scenario.scenario.get(key) for key in scenario_keys]
    )
    assert all_keys_equal
