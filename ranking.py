from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime

import pandas
import yaml


def generate_htmls():
    with open("config.yaml", "r") as f:
        configs = yaml.safe_load(f)
    users = configs["users"]

    def generate_table(score_text):
        ranking = {}
        titles = {}
        diffs = {}
        for user in users:
            csv_path = Path(f"{user}.csv")
            df = pandas.read_csv(csv_path)
            ranking[user] = float(df.iloc[-1, :][score_text])
            titles[user] = df.iloc[-1, :][f'{score_text}_name']
            if len(df) >= 2:
                diffs[user] = float(df.iloc[-1, :][score_text]) - \
                    float(df.iloc[-2, :][score_text])
            else:
                diffs[user] = 0

        sorted_users, sorted_scores = zip(*sorted(
            ranking.items(), key=lambda x: x[1], reverse=True))
        sorted_titles = [titles[user] for user in sorted_users]
        sorted_diffs = [diffs[user] for user in sorted_users]
        sorted_scores = [f"{_score} ({_diff:+.1f})" if _diff !=
                         0 else _score for _score, _diff in zip(sorted_scores, sorted_diffs)]
        df = pandas.DataFrame(
            {"Name": sorted_users, "Score": sorted_scores, "Titles": sorted_titles})
        df.index = [index + 1 for index in df.index]

        root1 = ET.fromstring(df.to_html(buf=None))
        root1.attrib['class'] = 'table table-bordered table-striped table-hover'
        root1.attrib.pop('border', None)
        root1.find('thead').find('tr').attrib.pop('style', None)
        return ET.tostring(root1, encoding='utf-8').decode()

    html = f"""<html lang="en">

    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>Shogi Wars Ranking</title>

    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <!-- JavaScript Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p"
        crossorigin="anonymous"></script>

    </head>
    <body>
    <h1 class='h1'>Shogi Wars Ranking</h1>
    <div style="width: 500px;padding-left: 20px">
    <p style="text-align: right;">{str(datetime.today().date())}</p>
    <h2>10 minutes rapid</h2>
    {generate_table('score1')}
    <h2>3 minutes rapid</h2>
    {generate_table('score2')}
    <h2>10 seconds</h2>
    {generate_table('score3')}
    </div>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == '__main__':
    generate_htmls()
