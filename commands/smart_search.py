# commands/smart_search.py

import webbrowser
import speech_recognition as sr
import threading
import time
from main import speak  # Import speak from your main.py

def run(assistant):
    try:
        # First, Assistant asks you
        assistant.is_awake = True
        if assistant.idle_timer:
            assistant.idle_timer.cancel()
        
        speak("What do you want me to search?")
        print("👂 Listening for search query...")

        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

        query = recognizer.recognize_google(audio)
        query = query.lower()
        print(f"🔍 Search Query: {query}")

        # Now perform Google Search
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(search_url)
        speak(f"Searching for {query}")

        assistant.reset_idle_timer()

    except sr.UnknownValueError:
        print("❓ Could not understand your search.")
        speak("Sorry, I didn't catch that. Please try again later.")
    except Exception as e:
        print(f"🚫 Error during search: {e}")
        speak("Something went wrong during the search.")
        # written by @GWSURYA