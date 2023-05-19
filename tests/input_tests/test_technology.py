from origin_sdk.service.InputsEditor import InputsEditor
from .utils_for_testing import (
    get_test_scenario_for_reading,
    testing_session as session,
    get_copy_of_readonly_scenario_for_updating,
)


def test_get_technology_names():
    s = get_test_scenario_for_reading()
    ie = InputsEditor(s.scenario_id, session)

    techs = ie.get_technology_names()

    assert techs is not None


def test_updating_all_capacities(project):
    # Init
    s = get_copy_of_readonly_scenario_for_updating("update all tech capacities")
    ie = InputsEditor(s.scenario_id, session)

    # Get the main region, and all the technology names for this region
    main_region = ie.inputs_session.get("productRegionInformation").get("code")
    tech_names_for_main_region = ie.get_technology_names().get(main_region).keys()

    # Now query all the technologies and store them by key. We will use this to
    # check which years to update values for
    all_tech_docs = {
        tech_name: ie.get_supply_technology(
            technology_name=tech_name, region=main_region
        )
        for tech_name in tech_names_for_main_region
    }

    # Helper function to access the capacity of the technology object (consider
    # adding helpers like this to the SDK as a native function)
    def get_capacity_from_tech(tech_doc):
        return tech_doc.get("getExogenous").get("parameters").get("capacity")

    # Log the responses, if any of these functions throw (service errors
    # included) then the test will fail, but we will also assert they all came
    # back with data and not a standard GQL "null" response
    update_tech_capacity_responses = [
        ie.update_exogenous_technology_variable(
            parameter="capacity",
            region=main_region,
            technology_name=tech_doc.get("name"),
            transform=[
                {
                    "year": year.get("year"),
                    "transform": {
                        "type": "Absolute",
                        "value": next(iter(get_capacity_from_tech(tech_doc))).get(
                            "original"
                        ),
                    },
                }
                for year in get_capacity_from_tech(tech_doc)
            ],
        )
        for tech_doc in all_tech_docs.values()
    ]

    # Assert they all have data
    assert all([res is not None for res in update_tech_capacity_responses])
