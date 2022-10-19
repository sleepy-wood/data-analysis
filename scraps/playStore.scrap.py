import numpy as np
import pandas as pd
from google_play_scraper import app, Sort, reviews_all


def scarp(country: str, app_name: str, app_id: int) -> None:
    reviews = reviews_all(
        app_id,
        sleep_milliseconds=1000,
        lang="en" if country == "us" else "ko",
        country=country,
        sort=Sort.NEWEST,
    )

    res_df = pd.DataFrame(np.array(reviews), columns=["review"])
    res_df = res_df.join(pd.DataFrame(res_df.pop("review").to_list()))
    res_df.to_csv(f"csvs/play-store/{app_name}_{country}.csv", index=False)


sleep_town = "seekrtech.sleep"
forest = "cc.forestapp"

country_list = ["kr", "us"]
app_name_list = ["sleep_town", "forest"]
app_id_list = [sleep_town, forest]

for i in range(len(app_id_list)):
    app_name = app_name_list[i]
    app_id = app_id_list[i]

    for country in country_list:
        scarp(country, app_name, app_id)
