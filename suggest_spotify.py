import os
import json
import openai
import spotipy
import logging
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

# base logger
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#region --- access token & Connection ---
load_dotenv()
OPEN_AI_TOKEN = os.environ.get("OPEN_AI_TOKEN")
SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_PLAYLIST_ID = os.environ.get("SPOTIFY_PLAYLIST_ID")
SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
# Connect Open AI
openai.api_key = OPEN_AI_TOKEN

# Connect Spotify
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = SPOTIFY_CLIENT_ID,
                                               client_secret = SPOTIFY_CLIENT_SECRET,
                                               redirect_uri = SPOTIFY_REDIRECT_URI,
                                               scope="playlist-modify-public"))
#endregion

#region --- Spotify Checker ---
def spotify_connect():
    print ("----------User-ID----------")
    user_id = spotify.me()['id']
    logging.log(logging.INFO, "Spotify User ID:" + user_id)
    print (user_id)
    print ("---------------------------")
#endregion

#region --- Suggest Music ---
def suggest_music(playlist_name ,msg):

    playlist_name = f"{ playlist_name }"
    user_id = spotify.me()['id']
    playlist = spotify.user_playlist_create(user_id, playlist_name)

    print ("------New-PlayList-ID------")
    print (playlist["name"],"-",playlist["id"])
    logging.log(logging.INFO, "New Spotify Playlist ID:" + playlist["name"] + "-" + playlist["id"])
    print ("---------------------------")

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Give me 10 list music {msg}",
        temperature=0.9,
        max_tokens=4000,
        top_p=1.0,
        frequency_penalty=0.9,
        presence_penalty=0.9,
        stop=["11"]
    )

    with open("./result.json", "w") as output_file:
        json.dump(response, output_file)
    
    with open('./result.json', 'r') as f:
        data = json.load(f)
    choices = data["choices"][0]["text"].strip()

    with open("./result.txt", "w") as f:
        for item in choices.split("\n"):
            replace_number = item.translate(str.maketrans("", "", ".0123456789"))
            song_name = replace_number.split(' by ')[0]
            # artist_name = replace_number.split(' by ')[1]
            selected_text = song_name.replace('"', '')
            f.write(selected_text + "\n")

            track_name = selected_text + "\n"
            query = f"{track_name}"
            results = spotify.search(q=query, type="track", limit=1)
            track_uri = results['tracks']['items'][0]['uri']
            print(track_uri)
    
            spotify.playlist_add_items(playlist['id'], [track_uri])
            logging.log(logging.INFO, "Added to Spotify Playlist:" + playlist["name"] + "-" + track_name + track_uri)
            # spotify.playlist_add_items(os.environ.get("SPOTIFY_PLAYLIST_ID"), [track_uri])

    # get user playlist
    print(playlist["name"],"-",playlist["id"], playlist["external_urls"]["spotify"])
    logging.log(logging.INFO, "Create Spotify Playlist Success:" + playlist["name"] + "-" + playlist["id"] + playlist["external_urls"]["spotify"])
    return playlist["external_urls"]["spotify"]
#endregion