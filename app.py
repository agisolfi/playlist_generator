from flask import Flask, redirect, request, session, url_for, render_template, g
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from openai import OpenAI
import ast
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Spotify API configuration
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "playlist-modify-public playlist-modify-private"
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

#  Authenticate OPENAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)
auth_manager.refresh_access_token(refresh_token=REFRESH_TOKEN)
sp=spotipy.Spotify(auth_manager=auth_manager)


def get_song_url(song_name, artist):
    query = f"{song_name} {artist}"
    results = sp.search(q=query, type="track", limit=1)  # Search for the track
    tracks = results.get("tracks", {}).get("items", [])
    if tracks:
        return tracks[0]['external_urls']['spotify']  # Return the track's sportify url
    else:
        print(f"Song '{song_name}' by '{artist}' not found.")
        return None
    
def build_url_list(song_list):
    song_urls=[]

    for song in song_list:
        url=get_song_url(song["name"],song["artist"])
        song_urls.append(url)
    print("URLS Recieved")
    return song_urls

def build_playlist(user_request,name):
    # Create a new playlist
    user_id = sp.me()["id"]  

    playlist_name = name
    playlist_description = f"A playlist generated based on ChatGPT recommendations from the following prompt:{user_request}."
    playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=True,  # Set to False for a private playlist
        description=playlist_description
    )
    print("Playlist Initialized")
    return playlist

def add_to_playlist(playlist_id,song_urls):
    sp.playlist_add_items(playlist_id=playlist_id,items=song_urls)
    print("songs added")

def get_chatgpt_recs(user_request):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", 
            "content": '''You are to act as a playlist generator, generating a list of songs at the request of the user. Please return a song list in the following format: {"name": "", "artist": " "}. Please seperate each song in the list with a comma. Please do not add any additional words besides this list.'''
            },
            {
                "role": "user",
                "content": user_request
            }
        ],
        model="gpt-4o",
    )
    print("Recommendations Built Successfully")
    print(chat_completion.choices[0].message.content)
    data=chat_completion.choices[0].message.content
    data=data.strip("'")
    song_list=ast.literal_eval(data)
    return song_list



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_playlist():
    # Get user inputs from the form
    user_request = request.form.get("request-input")
    playlist_name = request.form.get("playlist-name")

    songs = get_chatgpt_recs(user_request)
    playlist = build_playlist(user_request, playlist_name)
    song_urls = build_url_list(songs)
    add_to_playlist(playlist_id=playlist["id"], song_urls=song_urls)

    # Extract playlist link
    playlist_link = playlist["external_urls"]["spotify"]
    playlist_id = playlist["id"]  

    return render_template("success.html", playlist_name=playlist_name, playlist_link=playlist_link, length=len(songs),playlist_id=playlist_id)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
