from origin_sdk.OriginSession import OriginSession
from origin_sdk.service.Scenario import Scenario

session = OriginSession()
deu_scenario = Scenario("3549f685-ac8e-4e03-b383-b331cd0b7afd", session)

regions = deu_scenario.get_downloadable_regions()

all_downloads = {r: deu_scenario.get_download_types(r) for r in regions}

csv = deu_scenario.download_output_csv("deu", "system", "1y", "eur2021")
print(csv)

print(all_downloads)
