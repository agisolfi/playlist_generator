# ChatGPT Playlist Generator
Welcome to the ChatGPT Playlist Generator! This project was created using Spotify and OpenAI API services to allow users to directly create playlists formed through ChatGPT requests.
## Use
### Script for Personal Use
Users can use the playlist_generator.py script to generate their own playlists using ChatGPT. 

The requirements.txt can be used to create the corresponding python enviroment for this project.

`pip install -r requirements.txt` (Once an enviroment has been created and activated)

Users must pass the following enviroment variables: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and OPENAI_API_KEY from thier respective API accounts. 

Enviroment variables can be passed by running the following code in your enviroment's terminal:
`export SPOTIFY_CLIENT_ID="Insert-key-here"`

A localhost server will need to be hosted temporarily for Spotify's API to authenticate the user. Do so using the following line of code:

`python3 -m http.server 8000`

The program can now be run and the user will be prompted for a chatGPT request and an accompanying name for the playlist. The user can now check thier spotify and see the playlist added to their account.

For those who use Apple Music, you can download the free app SongShift on your phone and convert these playlists through the app.

### Live App
For those interesting in just using or experimenting with the playlist generator and do not wish to set up thier own Spotify/OpenAi development accounts, I have created a flask app hosted [here](https://playlist-generator-xjq7.onrender.com/) using Render for this purpose. 

