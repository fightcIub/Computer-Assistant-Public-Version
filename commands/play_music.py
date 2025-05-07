import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time
import subprocess
import platform
import webbrowser

# Setup Spotipy
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="", #change this to your client id
    client_secret="", #change this to your client secret
    redirect_uri="http://localhost:8888/callback",
    scope="user-read-playback-state,user-modify-playback-state,playlist-read-private,user-read-currently-playing,user-library-read"
))


# === Main RUN function ===
def run(assistant, song_name=None, playlist=None, control_command=None):
    try:
        ensure_active_device()

        if playlist:
            play_liked_songs()
            return

        if song_name:
            play_specific_song(song_name)
            return

        if control_command:
            handle_control_command(control_command)
            return

        # If no input, just resume
        resume_song()

    except Exception as e:
        print(f"Unexpected error: {e}")

# === NEW function ===
def ensure_active_device():
    devices = sp.devices().get('devices', [])
    active_device = None

    for device in devices:
        if device.get('is_active'):
            active_device = device
            break

    if not active_device:
        print("⚠️ No active Spotify device found. Trying to launch Spotify app...")
        launch_spotify()

        # Wait a bit for the app to start
        time.sleep(5)

        devices = sp.devices().get('devices', [])
        if not devices:
            print("❌ Still no device found. Please manually open Spotify and play a song.")
            webbrowser.open("https://open.spotify.com")
            raise Exception("No active device found.")

def launch_spotify():
    os_name = platform.system()

    if os_name == "Windows":
        # Open Spotify app
        subprocess.Popen(["start", "spotify:"], shell=True)

        # Give it a moment to open
        time.sleep(3)

        # Open a random Spotify song/playlist via URI (forces playback)
        webbrowser.open("https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT")  # Rickroll forever 😎
        
    elif os_name == "Darwin":  # MacOS
        subprocess.Popen(["open", "-a", "Spotify"])
        time.sleep(3)
        webbrowser.open("https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT")
        
    elif os_name == "Linux":
        subprocess.Popen(["spotify"])
        time.sleep(3)
        webbrowser.open("https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT")

    else:
        print("Unsupported OS for auto-launch. Please open Spotify manually.")

# === Helper Functions ===

def play_specific_song(song_query):
    results = sp.search(q=song_query, type="track", limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        track_uri = tracks[0]['uri']
        sp.start_playback(uris=[track_uri])
        print(f"Playing {tracks[0]['name']}...")
    else:
        print("Song not found.")

def play_liked_songs():
    try:
        results = sp.current_user_saved_tracks(limit=50)
        track_uris = [item['track']['uri'] for item in results['items']]
        
        if track_uris:
            sp.start_playback(uris=track_uris)
            print("Playing your Liked Songs!")
        else:
            print("No liked songs found.")
    except Exception as e:
        print(f"Error playing liked songs: {e}")

def handle_control_command(command):
    command = command.lower()

    if "skip" in command or "next" in command:
        skip_song()
    elif "previous" in command or "back" in command:
        previous_song()
    elif "pause" in command:
        pause_song()
    elif "resume" in command or "play" in command:
        resume_song()
    elif "volume up" in command:
        change_volume(up=True)
    elif "volume down" in command:
        change_volume(up=False)
    elif "shuffle" in command:
        toggle_shuffle()
    elif "repeat" in command:
        toggle_repeat()
    else:
        print(f"Unknown control command: {command}")

def skip_song():
    sp.next_track()
    print("Skipped to next song.")

def previous_song():
    sp.previous_track()
    print("Going to previous song.")

def pause_song():
    sp.pause_playback()
    print("Paused playback.")

def resume_song():
    sp.start_playback()
    print("Resumed playback.")

def change_volume(up=True):
    devices = sp.devices().get('devices', [])
    if devices:
        device = devices[0]
        current_volume = device.get('volume_percent', 50)
        new_volume = min(100, current_volume + 10) if up else max(0, current_volume - 10)
        sp.volume(new_volume)
        print(f"Volume changed to {new_volume}%")
    else:
        print("No active device found.")

def toggle_shuffle():
    current = sp.current_playback()
    if current:
        shuffle_state = current.get('shuffle_state', False)
        sp.shuffle(state=not shuffle_state)
        print(f"Shuffle {'enabled' if not shuffle_state else 'disabled'}.")
    else:
        print("No playback found.")

def toggle_repeat():
    current = sp.current_playback()
    if current:
        repeat_state = current.get('repeat_state', 'off')
        if repeat_state == "off":
            sp.repeat('track')  # Repeat current track
            print("Repeat current track enabled.")
        else:
            sp.repeat('off')
            print("Repeat turned off.")
    else:
        print("No playback found.")
# written by @GWSURYA