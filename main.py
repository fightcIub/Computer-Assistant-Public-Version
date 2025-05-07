import os
import importlib
import threading
import time
import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk, ImageSequence
import pygame
import speech_recognition as sr
import requests
from gtts import gTTS
import json
import random
import math





# === SETTINGS ===
API_KEY = "place_api_token_here" #get a free key from https://api.electronhub.top/ and replace it here
BASE_URL = "https://api.electronhub.top/v1/chat/completions"    #use any url you want, but make sure to use the same one in the API_KEY
# === Sounds ===  
POPUP_SOUND = "popup.wav"
POPDOWN_SOUND = "popdown.wav"

# === Wake Word and AI Question Starters ===
# You can add more wake words or AI question starters to these lists
WAKE_WORDS = ["hey computer", "okay computer", "hi computer", "a computer", "he computer"]
AI_QUESTION_STARTERS = ["what", "how", "who", "when", "where", "why", "can you", "could you", "would you", "tell me"]

# === Commands ===
# You can add more commands and their respective triggers here
commands_map = {
    "todo_manager": ["todo", "open to do", "start to do", "to do"],
    "open_hianime": ["open high anime","open hianime","high anime","hianime", "start hi anime","start hianime"],
    "open_github": ["open github", "start github", "github", "hey computer open github", "hey computer start github"],
    "open_dashboard": ["open dashboard", "start dashboard", "dashboard"],
    "open_crunchyroll": ["open crunchyroll", "start crunchyroll", "crunchyroll"],
    "voice_typing": ["type", "type something", "start typing", "start voice typing"],
    "open_youtube": ["open youtube", "start youtube", "can you open youtube", "please open youtube", "hey computer open youtube", "youtube"],
    "open_discord": ["open discord", "start discord", "launch discord", "hey computer open discord", "discord"],
    "smart_search": ["search", "google search", "search something", "hey computer search"],
    "open_gmail": ["open gmail", "start gmail", "launch gmail", "hey computer open gmail", "gmail"],
    "check_weather": ["check weather", "weather", "what's the weather", "hey computer check weather", "check the weather"],
    "open_calculator": ["open calculator", "start calculator", "calculator please", "hey computer open calculator", "open calc", "calculator"],
    "open_chatgpt": ["chat", "gpt", "open gpt", "open chat", "start gpt", "open chat gpt","open chatgpt", "start chat gpt", "start chatgpt", "can you open chat gpt","can you open chatgpt", "please open chat gpt","please open chatgpt", "hey computer open chat gpt"],
}

commands_modules = {}
chat_history = [{"role": "system", "content": "You are a helpful AI assistant."}]
memory_file = "brain.json"

if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        memory = json.load(f)
else:
    memory = {}
pygame.mixer.init()






# === GUI Class ===
class AssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)

        # Set background to a unique color (e.g., hot pink)
        transparent_color = '#6698FE'  # Bright pink that won't be in your gif

        self.root.config(bg=transparent_color)
        self.root.attributes('-transparentcolor', transparent_color)

        self.center_window(320, 240)

        # Make the label background same transparent color
        self.label = tk.Label(root, bg=transparent_color, bd=0, highlightthickness=0)
        self.label.pack()

        original_gif = Image.open("animation.gif")
        self.frames = [ImageTk.PhotoImage(img.resize((320, 240), Image.LANCZOS)) for img in ImageSequence.Iterator(original_gif)]

        self.frame_index = 0
        self.is_awake = False
        self.idle_timer = None

        self.animate()



    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def animate(self):
        if self.is_awake:
            frame = self.frames[self.frame_index]
            self.label.config(image=frame)
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        else:
            self.label.config(image="")
        self.root.after(100, self.animate)

    def smooth_fade(self, fade_in=True):
        if fade_in:
            for i in range(0, 11):
                self.root.attributes('-alpha', i / 10)
                time.sleep(0.03)
        else:
            for i in range(10, -1, -1):
                self.root.attributes('-alpha', i / 10)
                time.sleep(0.03)

    def wake_up(self):
        if not self.is_awake:
            self.is_awake = True
            self.play_sound(POPUP_SOUND)
            self.root.deiconify()
            self.smooth_fade(fade_in=True)
            print("Assistant Awakened!")
        self.reset_idle_timer()

    def sleep(self):
        if self.is_awake:
            self.play_sound(POPDOWN_SOUND)
            self.smooth_fade(fade_in=False)
            self.is_awake = False
            self.root.withdraw()
            print("Assistant Sleeping...")

    def reset_idle_timer(self):
        if self.idle_timer:
            self.idle_timer.cancel()
        self.idle_timer = threading.Timer(15.0, self.sleep)
        self.idle_timer.start()

    def play_sound(self, file_path):
        try:
            sound = pygame.mixer.Sound(file_path)
            sound.play()
        except Exception as e:
            print(f"Sound error: {e}")






# === Load Commands ===
def load_commands():
    global commands_modules
    commands_dir = "commands"
    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module = importlib.import_module(f"commands.{module_name}")
            commands_modules[module_name] = module





# === Greetings the User === #
import datetime
def speak_random_greeting():
    now = datetime.datetime.now()
    hour = now.hour

    # Time-based greetings
    if 5 <= hour < 12:
        time_greeting = "Good morning Surya, what's your command?"
    elif 12 <= hour < 18:
        time_greeting = "Good afternoon Surya, what's your command?"
    else:
        time_greeting = "Good evening Surya, what's your command?"

    # Regular greetings
    casual_greetings = [
        "Hey Surya, what's your command?",
        "Hello Surya, how can I assist you?",
        "I'm listening, Surya.",
        "Yes Surya, tell me."
    ]

    # Mix both
    all_greetings = casual_greetings + [time_greeting]

    # Pick one randomly
    chosen_greeting = random.choice(all_greetings)
    speak(chosen_greeting)






# === Recognize Speech ===
def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🔧 Calibrating microphone for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(f"Calibration done. Energy threshold: {recognizer.energy_threshold}")

    while True:
        try:
            with mic as source:
                print("👂 Listening for wake word...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)

            text = recognizer.recognize_google(audio).lower()
            print(f"Detected Speech: {text}")

            if any(wake_word in text for wake_word in WAKE_WORDS):
                print("🛑 Wake word detected!")

                # Wake up animation (GIF on)
                assistant.wake_up()

                # Instead of beep, SPEAK custom greeting
                speak_random_greeting()

                # Now listen for full user command
                with mic as source:
                    print("🎤 Listening for your command...")
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)

                command_text = recognizer.recognize_google(audio).lower()
                print(f"🗣️ Command received: {command_text}")
                show_user_command(command_text)  # 👈 This line shows your voice input on screen

                # Handle the command
                handle_input(command_text)

                # Optional: Sleep again after command handled
                assistant.sleep()

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            print("❓ Couldn't understand audio.")
            continue
        except sr.RequestError as e:
            print(f"🚫 API error: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(5)








# === Handle Input ===
def handle_input(text):
    for wake_word in WAKE_WORDS:
        if wake_word in text:
            text = text.replace(wake_word, "").strip()

    if "my name is" in text:
        name = text.split("my name is")[-1].strip().capitalize()
        memory["name"] = name
        with open(memory_file, "w") as f:
            json.dump(memory, f)
        print(f"Saved your name: {name}")
        speak(f"Nice to meet you, {name}")
        return

    # === 🆕 Spotify-Only Music Control (Songs, Playlists, Commands) ===
    spotify_control_commands = ["pause", "resume", "skip", "next", "previous", "back", "volume up", "volume down", "shuffle", "repeat"]
    
    if "play" in text:
        play_target = text.split("play", 1)[1].strip()

        if "playlist" in play_target:
            playlist_name = play_target.replace("playlist", "").strip()
            print(f"Detected playlist request: {playlist_name}")
            if "play_music" in commands_modules:
                assistant.is_awake = True
                if assistant.idle_timer:
                    assistant.idle_timer.cancel()
                commands_modules["play_music"].run(assistant, playlist=playlist_name)
                assistant.reset_idle_timer()
                return
        else:
            song_name = play_target
            print(f"Detected song request: {song_name}")
            if "play_music" in commands_modules:
                assistant.is_awake = True
                if assistant.idle_timer:
                    assistant.idle_timer.cancel()
                commands_modules["play_music"].run(assistant, song_name=song_name)
                assistant.reset_idle_timer()
                return

    elif any(cmd in text for cmd in spotify_control_commands):
        print(f"Spotify Control Command Detected: {text}")
        if "play_music" in commands_modules:
            assistant.is_awake = True
            if assistant.idle_timer:
                assistant.idle_timer.cancel()
            commands_modules["play_music"].run(assistant, control_command=text)
            assistant.reset_idle_timer()
            return
    # ================================================================

    # === Fallback: Other Registered Commands ===
    for command_name, triggers in commands_map.items():
        for trigger in triggers:
            if trigger in text:
                print(f"Executing command: {command_name}")
                if command_name in commands_modules:
                    assistant.is_awake = True
                    if assistant.idle_timer:
                        assistant.idle_timer.cancel()
                    commands_modules[command_name].run(assistant)
                    assistant.reset_idle_timer()
                    return

    # === AI Chat ===
    if any(text.startswith(word) for word in AI_QUESTION_STARTERS):
        assistant.is_awake = True
        if assistant.idle_timer:
            assistant.idle_timer.cancel()
        chat_with_ai(text)
        assistant.reset_idle_timer()
        return

    print("No command or AI detected.")





# === Show User Command GUI ===
# === Show User Command GUI (Floating Text, Centered, Clean Background) ===
def show_user_command(text):
    user_window = Toplevel()
    user_window.overrideredirect(True)
    user_window.attributes('-topmost', True)

    transparent_color = '#6698FE'
    user_window.configure(bg=transparent_color)
    user_window.attributes('-transparentcolor', transparent_color)

    screen_width = user_window.winfo_screenwidth()
    screen_height = user_window.winfo_screenheight()
    window_width = 700
    window_height = 150
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2) + 100  # slightly lower than AI response
    user_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Fade-in effect
    for i in range(0, 11):
        user_window.attributes("-alpha", i/10)
        user_window.update()
        time.sleep(0.02)

    label = tk.Label(
        user_window,
        text=text,
        bg=transparent_color,
        fg="#00ffff",  # cyan-style color for user input
        font=("Segoe UI", 16, "bold"),
        wraplength=680,
        justify="center"
    )
    label.pack(expand=True)

    # Auto-close after a few seconds
    def auto_close():
        time.sleep(2.5)
        user_window.destroy()
    threading.Thread(target=auto_close).start()




# === AI Chat with GUI Window ===
def chat_with_ai(user_input):
    chat_history.append({"role": "user", "content": user_input})

    try:
        response = requests.post(
            BASE_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": chat_history
            }
        )
        ai_response = response.json()['choices'][0]['message']['content']
        chat_history.append({"role": "assistant", "content": ai_response})

        show_ai_response(ai_response)

    except Exception as e:
        print("❌ Error:", e)








# === Show AI Typing GUI ===
# === Show AI Typing GUI (Floating Text, Centered, Clean Background) ===
def show_ai_response(text):
    ai_window = Toplevel()
    ai_window.overrideredirect(True)
    ai_window.attributes('-topmost', True)

    # Set a unique transparent color
    transparent_color = '#6698FE'
    ai_window.configure(bg=transparent_color)
    ai_window.attributes('-transparentcolor', transparent_color)

    # Center window
    screen_width = ai_window.winfo_screenwidth()
    screen_height = ai_window.winfo_screenheight()
    window_width = 900
    window_height = 700
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    ai_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Fade-in effect
    for i in range(0, 11):
        ai_window.attributes("-alpha", i/10)
        ai_window.update()
        time.sleep(0.03)

    # Display animated GIF (optional, at top)
    gif_label = tk.Label(ai_window, bg=transparent_color, bd=0, highlightthickness=0)
    gif_label.pack(pady=(10, 5))

    gif = Image.open("animation.gif")
    frames = [ImageTk.PhotoImage(img.resize((240, 180), Image.LANCZOS)) for img in ImageSequence.Iterator(gif)]

    def animate_gif(index):
        frame = frames[index]
        gif_label.configure(image=frame)
        index = (index + 1) % len(frames)
        ai_window.after(100, animate_gif, index)

    animate_gif(0)

    # Text floating directly with no background
    text_label = tk.Label(
        ai_window,
        text="",
        bg=transparent_color,
        fg="white",
        font=("Segoe UI", 16, "bold"),
        wraplength=560,
        justify="center",
        anchor="center",
        bd=0,
        highlightthickness=0
    )
    text_label.pack(pady=(20, 0), expand=True)

    # Typing animation
    def type_text():
        displayed_text = ""
        for char in text:
            displayed_text += char
            text_label.config(text=displayed_text + "▌")
            ai_window.update_idletasks()
            time.sleep(random.uniform(0.015, 0.035))
        text_label.config(text=displayed_text)

        speak(text)

        time.sleep(2)
        ai_window.destroy()
        assistant.sleep()

    threading.Thread(target=type_text).start()










# === Speak Text ===
def speak(text):
    tts = gTTS(text=text, lang='en', tld='com')
    filename = "response.mp3"
    tts.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove(filename)






# === MAIN ===
if __name__ == "__main__":
    load_commands()

    root = tk.Tk()
    assistant = AssistantGUI(root)
    assistant.sleep()

    listener_thread = threading.Thread(target=recognize_speech)
    listener_thread.daemon = True
    listener_thread.start()

    root.mainloop()

#written by @gwsuryaYT (talk to me on discord) 
#git hub.com/GWSuryaYT      
#read the readme for more info