from origin_sdk.service.Scenario import Scenario
from origin_sdk.service.InputsEditor import InputsEditor

from .utils_for_testing import (
    get_test_scenario_for_reading,
    testing_session as session,
    get_copy_of_readonly_scenario_for_updating,
)


def test_can_get_commodities():
    s = get_test_scenario_for_reading()
    ie = InputsEditor(s.scenario_id, session)
    cmdty = ie.get_commodities()

    assert cmdty is not None


def test_can_get_a_single_commodity():
    s = get_test_scenario_for_reading()
    ie = InputsEditor(s.scenario_id, session)
    gas = ie.get_commodities(commodities=["gas"])[0]

    assert gas.get("commodity") == "gas"


def test_updating_gas_price(project):
    s = get_copy_of_readonly_scenario_for_updating("update global gas prices to 666")
    ie = InputsEditor(s.scenario_id, session)

    # Get global gas
    # main_region = ie.inputs_session.get("productRegionInformation").get("code")
    gas = ie.get_commodities(commodities=["gas"])[0]
    assert gas.get("commodity") == "gas"

    before_update_tx = [year.get("transform") is None for year in gas.get("prices")]
    assert all(before_update_tx)

    gas_regions = gas.get("regions")
    gas_years = [year.get("year") for year in gas.get("prices")]

    # Make gas the devil's price
    after_update_gas = ie.update_commodity_price(
        commodity="gas",
        regions=gas_regions,
        transform=[
            {"year": year, "transform": {"type": "Absolute", "value": 666}}
            for year in gas_years
        ],
    )

    assert after_update_gas is not None

    after_update_tx = [
        year.get("transform") is not None for year in after_update_gas.get("prices")
    ]

    assert all(after_update_tx)


def test_rebasing_commodities(project):
    s = get_copy_of_readonly_scenario_for_updating(
        "replace commodity prices with last year's central case"
    )
    ie = InputsEditor(s.scenario_id, session)
    ie.get_commodities()
    ie.refresh()

    data_groups = ie.inputs_session.get("dataGroups")
    commodities_data_group = data_groups["commodities"]
    default_data_group = data_groups["default"]
    assert commodities_data_group["reference"] == default_data_group["reference"]

    rebase_scenario = Scenario.get_latest_scenario_from_region(
        s.session, region="gbr", name_filter=["net zero"]
    )
    rebase_id = rebase_scenario.scenario_id

    ie.change_base_commodities_assumptions(rebase_id)

    # Perform a GET as a follow up, to make sure the rebase completes and the
    # system is in a stable state
    ie.get_commodities(commodities=["gas"])

    ie.refresh()

    post_update_data_groups = ie.inputs_session.get("dataGroups")
    post_update_commodities_data_group = post_update_data_groups["commodities"]
    post_update_default_data_group = post_update_data_groups["default"]

    assert (
        post_update_commodities_data_group["reference"] == rebase_id
    ), "Rebase ID not set to commodities reference"
    assert (
        post_update_commodities_data_group["reference"]
        != post_update_default_data_group["reference"]
    ), "Commodities References and Default Reference still equal"
