from bs4 import BeautifulSoup
from pprint import pprint
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ----------- SPOTIFY APIs -------------
CLIENT_ID = "37ae617cbeec48d8baaac9d9cea44df4"
CLIENT_SECRET = "3374c8c5d7d9403ca29ef017aedaa5a3"

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

artist_tags = soup.select(selector=f"li > h3#{TITLE_ID} + span")
artists = [tag.string[4:][:-1] for tag in artist_tags]

print(f"Selected these songs for you:\n")
for idx in range(len(titles)):
    print(f"{titles[idx]} by {artists[idx]}")
print("\n")

# --------------- AUTH SPOTIFY APP --------------
print("[+] Logging into your spotify account...\n")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="37ae617cbeec48d8baaac9d9cea44df4",
    client_secret="3374c8c5d7d9403ca29ef017aedaa5a3",
    scope="playlist-modify-private",
    redirect_uri="http://example.com",
    show_dialog=True,
    cache_path="token.txt"))

USER_ID = sp.current_user()["id"]
print(f"[+] Done! Your user_id is {USER_ID}\n")


# --------------- CREATE PLAYLIST --------------
print(f"[+] Creating a playlist called 'Throwbacks from {user_date}'\n")

playlist_data = sp.user_playlist_create(
    user=USER_ID, name=f"Throwbacks from {user_date}", public="false")

# pprint(f"[+] Playlist data ---> {playlist_data}\n")
try:
    playlist_id = playlist_data["id"]
    print(f"[+] Done! Your playlist_id is {playlist_id}\n")
except:
    print("[!] Something went wrong creating the playlist\n")

# --------------- SEARCH FOR SONGS --------------
print("[+] Searching for selected songs on Spotify... \n")

uri_list = []
for title in titles:
    query = f"track: {title} year: {user_date[:4]}"
    result = sp.search(q={query}, type='track')
    # pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uri_list.append(uri)
        print(f"[+] Found '{title}'. Track_id is {uri}")
    except:
        print(f"[!] Something went wrong while searching for {title}")
        pprint(result)

print("\n")
pprint(f"Total songs found {len(uri_list)}")
print("\n")
# pprint(uri_list)

# --------------- ADD SONGS TO PLAYLIST --------------
print(f"Attempting to add songs to 'Throwbacks from {user_date}'\n")
add_to_playlist_response = sp.playlist_add_items(playlist_id, uri_list)
pprint(f"[+] Done!. Response data: {add_to_playlist_response}\n")
