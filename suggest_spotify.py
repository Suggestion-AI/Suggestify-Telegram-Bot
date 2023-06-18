import os
import openai
import spotipy
from logger import get_logger
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from llm.openai import open_ai_llm_completion_handler

# base logger
logger = get_logger(__name__)

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
    logger.info("Suggestify Running .... ")
    logger.info("Spotify User ID:" + user_id)
    print ("---------------------------")
#endregion

#region --- Suggest Music ---
def suggest_music(playlist_name ,msg):

    playlist_name = f"{ playlist_name }"
    user_id = spotify.me()['id']
    playlist = spotify.user_playlist_create(user_id, playlist_name)

    print ("------New-PlayList-ID------")
    print (playlist["name"],"-",playlist["id"])
    logger.info("New Spotify Playlist ID:" + playlist["name"] + "-" + playlist["id"])
    print ("---------------------------")

    print ("-----------Prompt----------")
    with open("./llm/prompts/spotify_playlist_generator.txt", "r") as f:
        prompt = f.read()
        response = open_ai_llm_completion_handler(f"{prompt}"+f"Your initial prompt will be: {msg}")
    print ("---------------------------")

    # write response to txt file 
    with open("./result.txt", "w") as f:
        response = response.strip().translate(str.maketrans("", "", ".0123456789"))
        response = response.replace('by', '-')
    
        for song in response.split('\n')[4:]:
            song_name = song
            f.write(song_name + "\n")

    with open('./result.txt', 'r') as input_file:
        file_contents = input_file.readlines()

        for song in file_contents:
            track_name = song.strip()
            query = f"{track_name}"
            results = spotify.search(q=query, type="track", limit=1)
            track_uri = results['tracks']['items'][0]['uri']
            print(track_uri)
    
            spotify.playlist_add_items(playlist['id'], [track_uri])
            logger.info("Added to Spotify Playlist:" + playlist["name"] + "-" + track_name + track_uri)

    # get user playlist
    logger.info("Create Spotify Playlist Success:" + playlist["name"] + "-" + playlist["id"] + playlist["external_urls"]["spotify"])
    return playlist["external_urls"]["spotify"]
#endregion