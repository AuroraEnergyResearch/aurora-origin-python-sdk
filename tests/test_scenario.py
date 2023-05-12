from origin_sdk.OriginSession import OriginSession
from origin_sdk.service.Scenario import Scenario

session = OriginSession()

# Construct the Scenario object with an ID
deu_scenario = Scenario("3549f685-ac8e-4e03-b383-b331cd0b7afd", session)

regions = deu_scenario.get_downloadable_regions()

all_downloads = {r: deu_scenario.get_download_types(r) for r in regions}

deu_region = all_downloads.get("deu")

all_deu_downloads = (
    [
        (item.get("type"), item.get("granularity"))
        for item in deu_region
        if item is not None
    ]
    if deu_region is not None
    else []
)

all_dfs = {
    f"{type}-{granularity}": deu_scenario.get_scenario_dataframe(
        "deu", type, granularity
    )
    for type, granularity in all_deu_downloads
}

test_scenario = None


def get_scenario_for_testing():
    global test_scenario
    if test_scenario is None:
        test_scenario = Scenario.get_latest_scenario_from_region(
            session=session, region="gbr"
        )

    return test_scenario


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


def test_construct_latest_gbr_scenario():
    get_scenario_for_testing()
    # The constructor passed, we are good to go
    assert True


def test_downloadable_regions_function():
    scenario = get_scenario_for_testing()
    regions = scenario.get_downloadable_regions()
    assert type(regions) == list
    assert len(regions) > 0


def test_get_scenario_region_function():
    scenario = get_scenario_for_testing()
    regions = scenario.get_downloadable_regions()
    all_info = [scenario.get_scenario_region(region) for region in regions]
    assert len([info for info in all_info if info is not None]) > 0


def test_get_download_types():
    scenario = get_scenario_for_testing()
    regions = scenario.get_downloadable_regions()
    download_types = {region: scenario.get_download_types(region) for region in regions}
    assert len(download_types) == len(regions)


def test_get_data_dfs():
    scenario = get_scenario_for_testing()
    regions = scenario.get_downloadable_regions()
    download_types = {region: scenario.get_download_types(region) for region in regions}

    yearly_dfs = [
        scenario.get_scenario_dataframe(
            region,
            type_granularity_combo.get("type"),
            type_granularity_combo.get("granularity"),
        )
        for region in regions
        for type_granularity_combo in download_types.get(region)
        if type_granularity_combo.get("granularity") == "1y"
    ]

    assert all([df is not None for df in yearly_dfs])


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
