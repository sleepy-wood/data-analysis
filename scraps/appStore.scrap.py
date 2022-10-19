import pandas as pd
from app_store_scraper import AppStore


def scarp(country: str, app_name: str, app_id: int) -> None:
    app = AppStore(country=country, app_name=app_name, app_id=app_id)
    app.review(sleep=1)

    res_df = pd.DataFrame(app.reviews)
    res_df.to_csv(f"csvs/app-store/{app_name}_{country}.csv", index=False)


auto_sleep = 1164801111
sleep_town = 1210251567
forest = 866450515

country_list = ["kr", "us"]
app_name_list = ["auto_sleep", "sleep_town", "forest"]
app_id_list = [auto_sleep, sleep_town, forest]

for i in range(len(app_id_list)):
    app_name = app_name_list[i]
    app_id = app_id_list[i]

    for country in country_list:
        scarp(country, app_name, app_id)
