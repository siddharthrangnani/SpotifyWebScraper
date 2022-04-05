from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
load_dotenv()

# Scraping Billboard 100
date = input(
    "Enter the Date in YYYY-MM-DD format to \n fetch top Charts from billBoard to Spotify Account")


response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
soup = BeautifulSoup(response.text, 'html.parser')


# List of songs
song_list_raw = soup.select(selector="div ul li ul li h3")
song_list = []
for s in range(99):
    song_list.append(song_list_raw[s].getText().replace('\n', ''))


# List of artists
span_class = "c-label a-no-trucate a-font-primary-s lrv-u-font-size-14@mobile-max u-line-height-normal@mobile-max u-letter-spacing-0021 lrv-u-display-block a-truncate-ellipsis-2line u-max-width-330 u-max-width-230@tablet-only"
artist_list_raw = soup.select(
    selector="div ul li ul li span", class_=span_class)
artist_list = []
for a in range(0, 99):

    artist_list.append(artist_list_raw[a].getText().replace('\n', ''))


# Zip songs and artists
songs_artists = list(zip(song_list, artist_list))


# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.getenv('CLIENT_ID'),
        client_secret=os.getenv('CLIENT_API'),
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# Searching Spotify for songs by TITLE AND ARTIST!
song_uris = []
for n in range(99):
    result = sp.search(
        q=f"track:{songs_artists[n][0]} artist:{songs_artists[n][1]}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except IndexError:
        print(f"{songs_artists[n][0]} doesn't exist in Spotify. Skipped.")
res1=sp.artist("https://open.spotify.com/artist/246dkjvS1zLTtiykXe5h60")
res1=res1["name"]
artist_uris = []
for n in range(15):
    result = sp.search(
        q=f"artist:{res1}", type="track")

    try:
        uri = result["tracks"]["items"][n]["uri"]
        artist_uris.append(uri)

    except IndexError:
        print("Song Doesnt Exist")
# Creating a new private playlist in Spotify for billboard
playlist = sp.user_playlist_create(
    user=user_id, name=f"{date} Billboard 100", public=False)


# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


# Creating a new private playlist in Spotify for artist
playlist1 = sp.user_playlist_create(
    user=user_id, name=f"{date} artist", public=False)

# Adding songs found into the new playlist for artist
sp.playlist_add_items(playlist_id=playlist1["id"], items=artist_uris)

