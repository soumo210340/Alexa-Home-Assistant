import requests
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import openai

# OpenAI API key
OPENAI_API_KEY = " "
openai.api_key = OPENAI_API_KEY

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# WeatherAPI key
API_KEY = " "

def talk(text):
    engine.say(text)
    engine.runAndWait()
    
def take_command():
    try:
        print('Listening...')
   
        with sr.Microphone() as source:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except Exception as e:
        print(e)
        return ""
    return command

# Function for weather 
def get_weather(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    data = response.json()
    weather = data['current']['condition']['text']
    temperature = data['current']['temp_c']
    return weather, temperature

def get_openai_response(question):
    response = openai.Completion.create(
        engine="davinci", prompt=question, max_tokens=100
    )
    return response.choices[0].text.strip()

def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('who is', '')
        try:
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk("Multiple matches found. Please specify.")
        except wikipedia.exceptions.PageError as e:
            talk("Sorry, I couldn't find any information.")
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
   
    
    else:
        response = get_openai_response(command)
        talk(response)

while True:
    run_alexa()                                                                                                     
