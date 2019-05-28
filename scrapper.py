from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

SHOW_ID = "tt0944947"
SHOW_URL = f'https://www.imdb.com/title/{SHOW_ID}/episodes'
SEASONS = 0


def get_seasons():
    seasons_page = urlopen(SHOW_URL)
    html = seasons_page.read()
    seasons_page.close()
    seasons_bs = bs(html, "html.parser")
    season_options = seasons_bs.find(id="bySeason").find_all("option")
    SEASONS = season_options


get_seasons()
