from bs4 import BeautifulSoup
from pprint import pprint
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ----------- SPOTIFY APIs -------------
CLIENT_ID = "37ae617cbeec48d8baaac9d9cea44df4"
CLIENT_SECRET = "3374c8c5d7d9403ca29ef017aedaa5a3"
SPOTIFY_URL = "https://api.spotify.com"
USER_ID = None
CREATE_PLAYLIST_API = f"/v1/users/{USER_ID}/playlists"
SCOPE = "playlist-modify-private"
LIB_SCOPE = "user-library-read"
REDIRECT_URI = "http://example.com"

# ----------- USER DATE -------------
user_date = input(
    "Which year would you want to travel to? Type the date in this format YYYY-MM-DD\n")

# ----------- FETCH SONGS -------------
BILLBOARD_URL = f"https://www.billboard.com/charts/hot-100/{user_date}"
response = requests.get(BILLBOARD_URL)
html = response.text
soup = BeautifulSoup(html, "html.parser")
# print(soup)

# ----------- SCRAPE & PREP DATA -------------
TITLE_ID = "title-of-a-story"
title_tags = soup.select(selector=f"li > h3#{TITLE_ID}")
titles = [tag.string[14:][:-5] for tag in title_tags]
# pprint(titles)

artist_tags = soup.select(selector=f"li > h3#{TITLE_ID} + span")
artists = [tag.string[4:][:-1] for tag in artist_tags]
# pprint(artists)

# --------------- ACCESS SPOTIFY APP --------------
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="37ae617cbeec48d8baaac9d9cea44df4",
    client_secret="3374c8c5d7d9403ca29ef017aedaa5a3",
    scope="playlist-modify-private",
    redirect_uri="http://example.com",
    show_dialog=True,
    cache_path="token.txt"))

USER_ID = sp.current_user()["id"]
print(USER_ID)
