from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

SHOW_ID = "tt0944947"
SHOW_URL = f'https://www.imdb.com/title/{SHOW_ID}/episodes'


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
    season_page = urlopen(season_url)
    html = season_page.read()
    season_page.close()
    season_bs = bs(html, "html.parser")
    episodes = season_bs.find_all("div", class_="list_item")
    for episode in episodes:
        rating = episode.find("span", class_="ipl-rating-star__rating")
        print(rating.string)


seasons = get_seasons()
for season in seasons:
    get_season_ratings(season)
