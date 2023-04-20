from origin_sdk.OriginSession import OriginSession
from origin_sdk.service.Scenario import Scenario

session = OriginSession()

# Construct the Scenario object with an ID
deu_scenario = Scenario("3549f685-ac8e-4e03-b383-b331cd0b7afd", session)

regions = deu_scenario.get_downloadable_regions()

all_downloads = {r: deu_scenario.get_download_types(r) for r in regions}

all_deu_downloads = [
    (item.get("type"), item.get("granularity")) for item in all_downloads.get("deu")
]

all_dfs = {
    f"{type}-{granularity}": deu_scenario.get_scenario_dataframe(
        "deu", type, granularity
    )
    for type, granularity in all_deu_downloads
}
