import pandas as pd

from collections import Counter
from konlpy.tag import Okt
from wordcloud import WordCloud

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
    df = pd.read_csv(f"csvs/play-store/{app_name}_{country}.csv")

    result = []
    if country == "kr":
        for review in df["content"]:
            text = okt.normalize(review)
            morphs = okt.morphs(text)

            for word in morphs:
                if len(word) > 1 and word not in ko_stop_words:
                    result.append(word)
    else:
        for review in df["content"]:
            if type(review) == str:
                word_tokens = reg_token.tokenize(review)

                for word in word_tokens:
                    if len(word) > 1 and word not in en_stop_words:
                        result.append(lemmatizer.lemmatize(word))

    c = Counter(result)
    wc = WordCloud(background_color="white", font_path="malgun", min_word_length=3)
    gen = wc.generate_from_frequencies(c)
    gen.to_file(f"images/play-store/{app_name}_{country}_wc.png")


country_list = ["kr", "us"]
app_name_list = ["sleep_town", "forest"]

for i in range(len(app_name_list)):
    app_name = app_name_list[i]

    for country in country_list:
        draw(country, app_name)
