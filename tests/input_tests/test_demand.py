from origin_sdk.service.InputsEditor import InputsEditor
from origin_sdk.service.Scenario import Scenario
from .utils_for_testing import (
    get_copy_of_default_readonly_scenario_for_updating,
    get_copy_of_scenario_for_updating,
    get_default_test_scenario_for_reading,
    testing_session as session,
)


def test_get_demand_regions():
    s = get_default_test_scenario_for_reading()
    ie = InputsEditor(s.scenario_id, session)

    regs = ie.get_demand_regions()

    assert regs is not None


def test_get_demand():
    s = Scenario.get_latest_scenario_from_region(session, "gbr", name_filter="central")
    ie = InputsEditor(s.scenario_id, session)

    regs = ie.get_demand_regions()

    for reg in regs:
        dem = ie.get_demand_for_region(region=reg)
        assert dem is not None

        dem_techs = dem.get("technologies")
        assert dem_techs is not None


def test_get_all_regions_demand():
    s = Scenario.get_latest_scenario_from_region(session, "aus", name_filter="central")
    ie = InputsEditor(s.scenario_id, session)

    regs = ie.get_demand_regions()

    dem = session.get_demand(
        scenario_id=s.scenario_id,
        demand_filter={"regions": regs},
        aggregate_regions=True,
    )[0]
    assert dem is not None
    assert dem.get("region").split(",") == regs

    dem_techs = dem.get("technologies")
    assert dem_techs is not None


def test_get_demand_tech_names():
    return
    # This isn't supported by the service, throws a 500
    s = get_default_test_scenario_for_reading()
    ie = InputsEditor(s.scenario_id, session)

    techs = ie.get_demand_technology_names()
    assert techs is not None


def test_get_all_demand_techs():
    s = get_default_test_scenario_for_reading()
    ie = InputsEditor(s.scenario_id, session)

    techs = ie.get_demand_technologies()
    assert techs is not None


def test_update_all_main_region_items(project):
    # Init
    s = get_copy_of_default_readonly_scenario_for_updating(
        "update all main region items"
    )
    ie = InputsEditor(s.scenario_id, session)

    # Get the main region. Demand is one document per region, so get the
    # singylar demand document
    main_region = ie.inputs_session.get("productRegionInformation").get("code")
    demand_for_main_region = ie.get_demand_for_region(main_region)

    # Assert we have demand data before moving forwards
    assert demand_for_main_region is not None

    # Iterate through all the years to get a set of variables to update. We need
    # one update API call per variable, so do the info collect first.
    all_system_variables = set(
        system_variable
        for year in demand_for_main_region.get("variables")
        for system_variable, value in year.items()
        if system_variable != "year" and value is not None
    )

    # Iterate over and update the system level variables first
    system_update_responses = [
        ie.update_system_demand_variable(
            region=main_region,
            variable=var,
            transform=[
                {
                    "year": year.get("year"),
                    "transform": {"type": "Percentage", "value": 10},
                }
                # Create a TX for each year
                for year in demand_for_main_region.get("variables")
                # Where the value for that year is defined
                if year.get(var) is not None
            ],
        )
        # Iterate over the variables
        for var in all_system_variables
        # Don't update totalDemand since that makes this all a bit pointless
        if var != "totalDemand"
    ]

    # If any of the individual calls throw, the test will fail. In the case
    # where there is no service error, but the data comes back as "null", this
    # will also catch this case.
    assert all([res is not None for res in system_update_responses])

    # Now do almost the same thing but for the demand technologies
    all_techs_by_name = {
        technology.get("originTechnology").get("original"): technology
        for technology in demand_for_main_region.get("technologies")
    }

    # Iterate and call the update function
    tech_update_responses = [
        ie.update_demand_technology_variable(
            region=main_region,
            variable="totalDemand",
            transform=[
                {
                    "year": year.get("year"),
                    "transform": {"type": "Percentage", "value": 10},
                }
                # For each year in the technology
                for year in all_techs_by_name[tech_name].get("variables")
                # But filter where the total demand is not defined
                if year.get("totalDemand") is not None
            ],
            technology=tech_name,
        )
        # Iterate over and call for each demand technology
        for tech_name in all_techs_by_name.keys()
    ]

    # Same as above, a gate to check that the resolver didn't silently return a
    # malformed object and the resolver is "null" without throwing a service
    # error
    assert all([res is not None for res in tech_update_responses])


def test_update_total_demand_across_all_regions(project):
    aus = Scenario.get_latest_scenario_from_region(
        session, "aus", name_filter="central"
    )
    s = get_copy_of_scenario_for_updating(aus, "update all regions at once")
    ie = InputsEditor(s.scenario_id, session)
    last_year = s.scenario.get("years")[-1]
    regs = ie.get_demand_regions()

    update_response = ie.update_system_demand_variable(
        region=regs,
        variable="totalDemand",
        transform=[
            {
                "year": last_year,
                "transform": {"type": "Percentage", "value": 10},
            }
        ],
    )
    assert update_response is not None
    last_base_demand_year = update_response.get("variables")[-1].get("baseDemand")

    tx = last_base_demand_year.get("transform")
    assert tx is not None
    assert round(tx.get("value"), 0) == 10

    for tech_doc in update_response.get("technologies"):
        last_tech_demand_year = tech_doc.get("variables")[-1].get("totalDemand")
        tech_tx = last_tech_demand_year.get("transform")
        assert tech_tx is not None
        assert round(tech_tx.get("value"), 0) == 10
