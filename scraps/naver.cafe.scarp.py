import json
import argparse
import urllib.request

import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--id", type=str)
parser.add_argument("--secret", type=str)
parser.add_argument("--query", type=str)
args = parser.parse_args()

client_id = args.id
client_secret = args.secret
query = args.query
encText = urllib.parse.quote(query)

result = []
for i in range(1, 1000, 100):
    url = f"https://openapi.naver.com/v1/search/cafearticle?query={encText}&display=100&start={i}"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)

    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read()
        response_body = response_body.decode("utf-8")
        data = json.loads(response_body)

        for item in data["items"]:
            result.append(
                {
                    "title": item["title"],
                    "link": item["link"],
                    "description": item["description"],
                    "cafename": item["cafename"],
                    "cafeurl": item["cafeurl"],
                }
            )
    else:
        print("Error Code:" + rescode)
        continue


pd.DataFrame(result).to_csv(f"csvs/naver/cafe_{query}.csv", index=False)
