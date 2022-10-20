import numpy as np
import pandas as pd

from konlpy.tag import Okt

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer


korean_stopwords_path = "./korean_stopwords.txt"
with open(korean_stopwords_path, encoding="utf-8") as f:
    ko_stop_words = f.readlines()

ko_stop_words = [x.strip() for x in ko_stop_words]
okt = Okt()

reg_token = RegexpTokenizer("[\\w]+")
en_stop_words = stopwords.words("english")
lemmatizer = WordNetLemmatizer()


def draw(country: str, app_name: str) -> None:
    df = pd.read_csv(f"csvs/app-store/{app_name}_{country}.csv")
    df["result"] = np.nan

    if country == "kr":
        for index, review in enumerate(df["review"]):
            result = []
            text = okt.normalize(review)
            morphs = okt.morphs(text)

            for word in morphs:
                if len(word) > 1 and word not in ko_stop_words:
                    result.append(word)

            temp = " ".join(result)
            df.iloc[index, -1] = temp
    else:
        for index, review in enumerate(df["review"]):
            result = []
            word_tokens = reg_token.tokenize(review)

            for word in word_tokens:
                if len(word) > 1 and word not in en_stop_words:
                    result.append(lemmatizer.lemmatize(word))

            df.iloc[index, -1] = " ".join(result)

    df["result"].to_csv(
        f"csvs/app-store/{app_name}_{country}_result.csv", index=False, header=False
    )


country_list = ["kr", "us"]
app_name_list = ["auto_sleep", "sleep_town", "forest"]

for i in range(len(app_name_list)):
    app_name = app_name_list[i]

    for country in country_list:
        draw(country, app_name)
