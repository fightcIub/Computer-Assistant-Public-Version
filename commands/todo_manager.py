import json
import os
import speech_recognition as sr
from datetime import datetime
from main import speak

TODO_FILE = "todo_list.json"
recognizer = sr.Recognizer()
mic = sr.Microphone()

# === Main Entry Point ===
def run(assistant):
    try:
        # First, Assistant asks you
        assistant.is_awake = True
        if assistant.idle_timer:
            assistant.idle_timer.cancel()

        speak("Welcome to your to-do list manager. What would you like to do?")
        print("👂 Listening for to-do action...")

        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

        user_input = recognizer.recognize_google(audio).lower()
        print(f"📝 User Input: {user_input}")

        # Handle the user's input
        if any(word in user_input for word in ["add", "note", "remember"]):
            speak("Okay, what should I add?")
            print("👂 Listening for task to add...")

            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

            task = recognizer.recognize_google(audio).strip()
            print(f"➕ Task to Add: {task}")

            if task:
                add_task(assistant, task)
            else:
                speak("I didn't catch the task. Please try again.")

        elif any(word in user_input for word in ["show", "list", "what"]):
            list_tasks(assistant)

        elif any(word in user_input for word in ["clear", "remove", "delete"]):
            clear_tasks(assistant)  # Directly clear the tasks without confirmation

        else:
            speak("I didn't understand that. Try saying add a task, show my list, or clear it.")

        assistant.reset_idle_timer()

    except sr.UnknownValueError:
        print("❓ Could not understand your input.")
        speak("Sorry, I didn't catch that. Please try again.")
    except Exception as e:
        print(f"🚫 Error in To-Do Manager: {e}")
        speak("Something went wrong with the to-do manager.")

# === Helpers ===
def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TODO_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(assistant, task):
    tasks = load_tasks()
    tasks.append({
        "task": task,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_tasks(tasks)
    message = f"Task added: {task}"
    print(f"✅ {message}")
    speak(message)

def list_tasks(assistant):
    tasks = load_tasks()
    if not tasks:
        speak("Your to-do list is empty.")
        print("📭 Your to-do list is empty.")
    else:
        speak(f"You have {len(tasks)} tasks. Here they are:")
        print("📝 Your to-do list:")
        for i, entry in enumerate(tasks, 1):
            task = entry.get("task", "Unknown task")
            print(f"{i}. {task}")
            speak(f"{i}. {task}")

def clear_tasks(assistant):
    save_tasks([])
    message = "All tasks have been cleared."
    print(f"🧹 {message}")
    speak(message)
