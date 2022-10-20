from bs4 import BeautifulSoup
from pprint import pprint
import requests


user_date = input(
    "Which year would you want to travel to? Type the date in this format YYYY-MM-DD\n")
URL = f"https://www.billboard.com/charts/hot-100/{user_date}"

response = requests.get(URL)
html = response.text
soup = BeautifulSoup(html, "html.parser")
# print(soup)

TITLE_ID = "title-of-a-story"


title_tags = soup.select(selector=f"li > h3#{TITLE_ID}")
titles = [tag.string[14:][:-5] for tag in title_tags]
pprint(titles)

artist_tags = soup.select(selector=f"li > h3#{TITLE_ID} + span")
artists = [tag.string[4:][:-1] for tag in artist_tags]
pprint(artists)
