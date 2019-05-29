import io
from PIL import Image
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np

RATINGS = {}


def get_seasons(show_url):
    seasons_page = urlopen(show_url)
    html = seasons_page.read()
    seasons_page.close()
    seasons_bs = bs(html, "html.parser")
    season_count = seasons_bs.find(id="bySeason").find_all("option")
    seasons = []
    for i in range(1, len(season_count) + 1):
        url = f'{show_url}?season={i}'
        seasons.append(url)
    return seasons


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
        RATINGS[season_number].append(float(rating.string))


def make_graph():
    plt.xlabel('Episodes')
    plt.ylabel('Ratings')
    legends = []
    for season, ratings in RATINGS.items():
        plt.plot(range(1, len(ratings) + 1), ratings)
        legends.append(f'Season {season}')
    plt.xticks(np.arange(1, 11))
    plt.yticks(np.arange(4.5, 10.5, 0.5),)
    plt.legend(legends)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img = Image.open(buf)
    buf.close()
    return img


def main(show_id):
    show_url = f'https://www.imdb.com/title/{show_id}/episodes'
    seasons = get_seasons(show_url)
    for season in seasons:
        get_season_ratings(season)
    img = make_graph()
    return img
