import speech_recognition as sr
import pyttsx3
import os
import psutil
import webbrowser
import pywhatkit
import pyautogui
import requests
from bs4 import BeautifulSoup
import random
import subprocess

# AI Assistant Name
assistant_name = "PAX"

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

# Set Masculine Voice with American Accent
def set_male_voice():
    voices = engine.getProperty("voices")
    for voice in voices:
        if "male" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            print(f"Using male voice: {voice.name}")
            break

set_male_voice()

def check_internet():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except requests.ConnectionError:
        return False

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen(offline=False):
    recognizer = sr.Recognizer()
    try:
        # Automatically use the default microphone
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

            # Try Google Speech Recognition first
            if not offline:
                print("Recognizing with Google Speech Recognition...")
                try:
                    command = recognizer.recognize_google(audio).lower()
                    print(f"You said: {command}")
                    return command
                except sr.RequestError:
                    print("Google Speech Recognition failed. Trying offline mode...")
                    speak("Online recognition failed. Switching to offline mode.")

            # Fallback to PocketSphinx (offline)
            print("Recognizing with PocketSphinx...")
            try:
                command = recognizer.recognize_sphinx(audio).lower()
                print(f"You said (offline): {command}")
                return command
            except sr.UnknownValueError:
                print("PocketSphinx could not understand audio")
                speak("Sorry, I couldn't understand that.")
            except sr.RequestError as e:
                print(f"PocketSphinx error: {e}")
                speak("There seems to be an issue with the offline recognition service.")
    except sr.WaitTimeoutError:
        print("Listening timed out while waiting for phrase.")
        speak("I didn't hear anything. Please try again.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        speak("An error occurred while listening.")
    return None

def command_list():
    commands = [
        "open application: Opens a web application.",
        "play youtube: Plays a video on YouTube.",
        "play spotify: Plays a song on Spotify.",
        "create folder: Creates a new folder on the desktop.",
        "talk to me / chat with me: Casual conversation.",
        "tell me a fun fact: Shares a random fun fact.",
        "change name to <name>: Changes the assistant's name.",
        "what can you do / your features: Lists the assistant's capabilities.",
        "exit / stop: Stops the assistant."
    ]
    speak("Here are the available commands:")
    for command in commands:
        print(command)
        speak(command)

def open_web_application():
    if not check_internet():
        speak("No internet connection. Please check your network and try again.")
        return
    speak("Which web application would you like to open?")
    app_name = listen()
    known_apps = {
        "whatsapp": "https://web.whatsapp.com",
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://twitter.com",
        "gmail": "https://mail.google.com",
        "google drive": "https://drive.google.com",
        "linkedin": "https://www.linkedin.com",
        "hacker rank": "https://www.hackerrank.com",
        "leetcode": "https://leetcode.com",
        "github": "https://github.com",
        "stackoverflow": "https://stackoverflow.com",
        "spotify": "https://spotify.com",
        "amazon": "https://amazon.com"
    }
    app_name = app_name.strip() if app_name else ""
    if app_name in known_apps:
        url = known_apps[app_name]
        speak(f"Opening {app_name}")
        webbrowser.open(url)
    else:
        speak("I can only open known applications. Please try again with a listed application.")

def play_youtube_video():
    if not check_internet():
        speak("No internet connection. Please check your network and try again.")
        return
    speak("What do you want to watch on YouTube?")
    search_query = listen()
    if search_query:
        speak(f"Playing {search_query} on YouTube.")
        pywhatkit.playonyt(search_query)
    else:
        speak("I didn't catch that. Please say the name of the video again.")

def play_spotify_song():
    if not check_internet():
        speak("No internet connection. Please check your network and try again.")
        return
    speak("What song would you like to play on Spotify?")
    song_name = listen()
    if song_name:
        speak(f"Playing {song_name} on Spotify.")
        webbrowser.open(f"https://open.spotify.com/search/{song_name}")
    else:
        speak("I didn't catch that. Please say the song name again.")

def get_fun_fact():
    if not check_internet():
        speak("No internet connection. Cannot fetch a fun fact right now.")
        return
    try:
        response = requests.get("https://www.randomfunfacts.com/")
        soup = BeautifulSoup(response.text, "html.parser")
        fact = soup.find("i").text
        speak(f"Here's a fun fact: {fact}")
    except Exception as e:
        speak("I couldn't fetch a fun fact at the moment. Try again later.")
        print("Error fetching fun fact:", e)

def casual_talk():
    responses = [
        "I'm here to assist you! How's your day going?",
        "Tell me something interesting about your day!",
        "Do you want to hear a fun fact?",
        "I'm always ready for a chat. What’s on your mind?",
        "Life’s good when you have an AI assistant, right?"
    ]
    speak(random.choice(responses))

def execute_command(command):
    if command is None:
        return
    if "open application" in command:
        open_web_application()
    elif "play youtube" in command:
        play_youtube_video()
    elif "play spotify" in command:
        play_spotify_song()
    elif "fun fact" in command:
        get_fun_fact()
    elif "talk to me" in command or "chat with me" in command:
        casual_talk()
    elif "help" in command or "commands" in command or "features" in command:
        command_list()
    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I don't recognize that command. Please try again or say 'help' for a list of commands.")

if __name__ == "__main__":
    speak(f"Hello! My name is {assistant_name}. I'm ready to assist you.")
    while True:
        user_command = listen()
        execute_command(user_command)
