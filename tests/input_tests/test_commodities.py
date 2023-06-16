from origin_sdk.OriginSession import OriginSession
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


def test_updating_gas_price(project):
    s = get_copy_of_readonly_scenario_for_updating("update all tech capacities")
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
