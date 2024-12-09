import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from openai import OpenAI
import ast

SPOTIFY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Authenticate Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri="http://localhost:8000/callback",
    scope="user-read-private,playlist-modify-public,playlist-modify-private"  # Use 'playlist-modify-private' for private playlists
))

# Get the authenticated user's Spotify ID
user_id = sp.me()["id"]

# Authenticate OPENAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  
)
# Function to search for song url
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



#----------------------------------------------------------------#
if __name__=="__main__":
    user_request=input("Enter request for playlist. Ex: 'I want you to create a playlist of music similar to the Deftones song Cherry Waves.'\n")
    playlist_name=input("Enter the name for the playlist\n")

    songs = get_chatgpt_recs(user_request)
    playlist=build_playlist(user_request,playlist_name)
    song_urls=build_url_list(songs)
    add_to_playlist(playlist_id=playlist['id'],song_urls=song_urls)
    print("Playlist Made Sucessfully")

