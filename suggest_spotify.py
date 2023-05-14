import os
import json
import openai
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

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

def spotify_connect():
    print ("----------User-ID----------")
    user_id = spotify.me()['id']
    print (user_id)
    print ("---------------------------")

    print ("--------PlayList-ID--------")
    playlists = spotify.current_user_playlists()
    for playlist in playlists['items']:
        print(playlist["name"],"-",playlist["id"])
    print ("---------------------------")

def suggest_music(msg):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"10 lists suggest music piece that would accompany artwork nicely depending upon its {msg} type along ",
        temperature=0.9,
        max_tokens=4000,
        top_p=1.0,
        frequency_penalty=0.9,
        presence_penalty=0.9,
        stop=["11"]
    )

    with open("../result.json", "w") as output_file:
        json.dump(response, output_file)
    
    with open('../result.json', 'r') as f:
        data = json.load(f)
    choices = data["choices"][0]["text"].strip()

    with open("../result.txt", "w") as f:
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
    
            # spotify.playlist_add_items(playlist['id'], [track_uri])
            spotify.playlist_add_items(os.environ.get("SPOTIFY_PLAYLIST_ID"), [track_uri])

    # get user playlist
    playlists = spotify.current_user_playlists()
    for playlist in playlists['items']:
        print(playlist['name'])