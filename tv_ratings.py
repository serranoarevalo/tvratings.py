import io
from PIL import Image
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np

RATINGS = {}


def get_info(show_url):
    seasons_page = urlopen(show_url)
    html = seasons_page.read()
    seasons_page.close()
    seasons_bs = bs(html, "html.parser")
    season_count = seasons_bs.find(id="bySeason").find_all("option")
    title = seasons_bs.find(
        "div", class_="subpage_title_block").find("h3").find("a")
    seasons = []
    for i in range(1, len(season_count) + 1):
        url = f'{show_url}?season={i}'
        seasons.append(url)
    return (seasons, title.string)


def get_season_ratings(season_url):
    print(f'Getting: {season_url}')
    season_number = season_url[-1:]
    season_page = urlopen(season_url)
    html = season_page.read()
    season_page.close()
    season_bs = bs(html, "html.parser")
    episodes = season_bs.find_all("div", class_="list_item")
    RATINGS[season_number] = []
    for episode in episodes:
        rating = episode.find("span", class_="ipl-rating-star__rating")
        if rating:
            RATINGS[season_number].append(float(rating.string))


def make_graph(title):
    plt.xlabel('Episodes')
    plt.ylabel('Ratings')
    legends = []
    for season, ratings in RATINGS.items():
        if len(ratings) is not 0:
            plt.plot(range(1, len(ratings) + 1), ratings)
            legends.append(f'Season {season}')
    plt.xticks(np.arange(1, 11))
    plt.yticks(np.arange(0, 10.5, 0.5),)
    plt.legend(legends)
    plt.title(title)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def main(show_id):
    show_url = f'https://www.imdb.com/title/{show_id}/episodes'
    seasons, title = get_info(show_url)
    for season in seasons:
        get_season_ratings(season)
    img = make_graph(title)
    return img
