from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np

SHOW_ID = "tt0944947"
SHOW_URL = f'https://www.imdb.com/title/{SHOW_ID}/episodes'
RATINGS = {}

print("Visualizing the decline of GOT")


def get_seasons():
    seasons_page = urlopen(SHOW_URL)
    html = seasons_page.read()
    seasons_page.close()
    seasons_bs = bs(html, "html.parser")
    season_count = seasons_bs.find(id="bySeason").find_all("option")
    seasons = []
    for i in range(1, len(season_count) + 1):
        url = f'{SHOW_URL}?season={i}'
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
    print("Making Graph")
    plt.xlabel('Episodes')
    plt.ylabel('Ratings')
    legends = []
    for season, ratings in RATINGS.items():
        plt.plot(range(1, len(ratings) + 1), ratings)
        legends.append(f'Season {season}')
    plt.xticks(np.arange(1, 11))
    plt.yticks(np.arange(4.5, 10.5, 0.5),)
    plt.legend(legends)
    plt.show()
    print("Done!")


seasons = get_seasons()
for season in seasons:
    get_season_ratings(season)

make_graph()
