import webbrowser
from main import speak  # 🛠️ import speak
import speech_recognition as sr  # 🛠️ import sr for local listen

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

def run(assistant):
    speak("Do you have anything specific in mind for YouTube?")
    response = listen()

    if response.lower() in ["no", "na", "nah", "nope", "nothing"]:
        speak("Alright, opening YouTube home page.")
        webbrowser.open("https://www.youtube.com")
    else:
        speak("Alright, what would you like to watch?")
        search_query = listen()

        if search_query.strip() == "":
            speak("I didn't catch that. Opening YouTube home page.")
            webbrowser.open("https://www.youtube.com")
        else:
            search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
            speak(f"Searching YouTube for {search_query}.")
            webbrowser.open(search_url)

    assistant.sleep()
    