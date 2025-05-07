import speech_recognition as sr
import pyautogui
from main import speak
import time

def listen(timeout=5, phrase_time_limit=5):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            return recognizer.recognize_google(audio).lower()
        except (sr.UnknownValueError, sr.RequestError):
            return ""
        except sr.WaitTimeoutError:
            return ""

def confirm(prompt):
    speak(prompt)
    time.sleep(1)  # give time to prepare speaking
    for _ in range(2):
        print("🎤 Waiting for confirmation (say yes or no)...")
        response = listen(timeout=4, phrase_time_limit=4)
        print(f"Confirmation response: {response}")

        if any(word in response for word in ["yes", "yeah", "yup", "sure", "please do"]):
            return True
        if any(word in response for word in ["no", "nah", "nope", "don't"]):
            return False

        speak("Sorry, I didn't catch that. Can you say yes or no?")
    return False

def run(assistant):
    speak("Okay Surya, start speaking. I'll type for you.")
    typing_active = True

    while typing_active:
        text = listen(timeout=8, phrase_time_limit=8)
        print(f"Voice input: {text}")

        if not text:
            continue

        if "stop" in text:
            if confirm("Do you want me to stop typing? Please say yes or no."):
                speak("Okay, stopping typing now.")
                typing_active = False
            else:
                speak("Alright, I'll continue typing.")
                pyautogui.typewrite("stop ")
        else:
            pyautogui.typewrite(text + " ")
            time.sleep(0.2)  # Small pause so it feels natural
