import re
from datetime import datetime
from pathlib import Path
import time

import requests
from bs4 import BeautifulSoup
import yaml


def save_data():
    with open("config.yaml", "r") as f:
        configs = yaml.safe_load(f)
    users = configs["users"]

    print("saving data..")
    for user in users:
        url = f'https://shogiwars.heroz.jp/users/mypage/{user}'
        soup = BeautifulSoup(requests.get(url).content, 'lxml')

        percentages = soup.find_all("div", class_="progress_bar")
        dankyus = soup.find_all("td", class_="dankyu")

        scores = []
        for dankyu, percentage in zip(dankyus, percentages):
            if "級" in dankyu.text:
                rating_base = (16 - int(dankyu.text.replace('級', ''))) * 100
            elif '初段' in dankyu.text:
                rating_base = 1600
            elif '段' in dankyu.text:
                rating_base = (15 + int(dankyu.text.replace('段', ''))) * 100
            pattern = '.*?(\d+).(\d+)%.*'

            result = re.match(pattern, percentage.text.replace('\n', ''))
            percentage_text = percentage.text.replace(
                '\n', '').strip().replace('\u2009', ' ')
            score_name = f"""{dankyu.text}/{percentage_text}"""
            if result is not None:
                rating_detail = float(f"{result.group(1)}.{result.group(2)}")
                if rating_detail >= 20:
                    rating_detail = (rating_detail - 20) * 1.25
                else:
                    rating_detail = (rating_detail - 20) * 5
            scores.append(str(round(rating_base + rating_detail, 1)))
            scores.append(score_name)

        # save the data
        csv_path = Path(f"{user}.csv")
        if not csv_path.exists():
            with open(csv_path, 'w', encoding='utf-8') as f:
                f.write(
                    "date,score1,score1_name,score2,score2_name,score3,score3_name\n")
                f.write(",".join([str(datetime.today())] + scores) + "\n")
        else:
            with open(csv_path, 'a', encoding='utf-8') as f:
                f.write(",".join([str(datetime.today())] + scores) + "\n")
        time.sleep(15)


if __name__ == '__main__':
    pass
