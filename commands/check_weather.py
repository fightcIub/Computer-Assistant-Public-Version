import requests

# 🛑 Replace this with your own OpenWeatherMap API Key
API_KEY = ""

# 🛑 Set your home city
CITY = ""

def run(assistant):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            assistant.play_sound("popdown.wav")
            assistant.sleep()
            print(f"❌ Failed to fetch weather: {data.get('message', '')}")
            return

        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        weather_report = f"The weather in {CITY} is {weather} with a temperature of {temperature}°C, feels like {feels_like}°C."

        print("✅ Weather Fetched:", weather_report)
        assistant.is_awake = True
        if assistant.idle_timer:
            assistant.idle_timer.cancel()
        from main import speak
        speak(weather_report)
        assistant.reset_idle_timer()

    except Exception as e:
        print(f"❌ Error fetching weather: {e}")
# written by @GWSURYA

