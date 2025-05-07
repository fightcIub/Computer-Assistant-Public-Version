import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- FILL YOUR DETAILS ---
CLIENT_ID = "" # Fill in your Spotify API credentials here
CLIENT_SECRET = "" # Fill in your Spotify API credentials here
REDIRECT_URI = "http://localhost:8888/callback" # Dont change this unless you know what you're doing

# --- AUTHENTICATE ---
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
))

# --- TEST ---
current = sp.current_playback()

if current:
    print("Connected to Spotify!")
    print("Currently playing:", current['item']['name'])
else:
    print("Connected, but nothing is playing.")
    # written by @GWSURYA