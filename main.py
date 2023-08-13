import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy_client_information import *

URL = "https://www.billboard.com/charts/hot-100/"
spotipy_client_ID = Spotipy_client_ID
spotipy_client_secret = Spotipy_client_secret
Redirect_URI = "http://example.com"
OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'


# check_date = input("WHAT IS THE DATE WOULD YOU LIKE TO TRAVEL? PLEASE WRITE IN THE FORMAT OF yyy-mm-dd.")
# scrape the top 100 song titles
response = requests.get(url=URL)
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page,"html.parser")

# data_of_songs = soup.find_all(name="h3", id="title-of-a-story")
# # print(data_of_songs)
#
# songs_list = []
# first_song = data_of_songs[6].get_text().strip()
#
# songs_list.append(first_song)
#
# for index in range(10, len(data_of_songs)-4*4, 4):
#     name_of_song = data_of_songs[index].get_text().strip()
#     print(name_of_song)
#     songs_list.append(name_of_song)
# print(songs_list)

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

# Authentication with Spotify to access my spotify account

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=spotipy_client_ID,
        client_secret=spotipy_client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="Zhan SUN",
    )
)
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
song_names = ["The list of song", "titles from your", "web scrape"]

# Search Spotify for the Songs
song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#create a new private playlist with the name "YYYY-MM-DD Billboard 100"
# Add each of the songs found in Step 3 to the new playlist.

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
song_uris = ["The list of", "song URIs", "you got by", "searching Spotify"]

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)