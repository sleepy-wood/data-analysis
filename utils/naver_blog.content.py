import numpy as np
import pandas as pd

from konlpy.tag import Okt

korean_stopwords_path = "./korean_stopwords.txt"
with open(korean_stopwords_path, encoding="utf-8") as f:
    ko_stop_words = f.readlines()

ko_stop_words = [x.strip() for x in ko_stop_words]
okt = Okt()


def draw(query: str) -> None:
    df = pd.read_csv(f"csvs/naver/blog_{query}.csv")
    df["result"] = np.nan

    for index, description in enumerate(df["description"]):
        result = []
        if isinstance(description, str):
            text = okt.normalize(description)
            morphs = okt.morphs(text)

            for word in morphs:
                if len(word) > 1 and word not in ko_stop_words:
                    result.append(word)

            temp = " ".join(result)
            df.iloc[index, -1] = temp

    df["result"].to_csv(
        f"csvs/naver/blog_{query}_result.csv", index=False, header=False
    )


query_list = ["수면클리닉", "수면다원검사"]

for i in range(len(query_list)):
    query = query_list[i]
    draw(query)
