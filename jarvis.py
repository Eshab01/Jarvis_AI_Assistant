import g4f
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import psutil
import datetime
import json
from textblob import TextBlob

# Set up voice engine
engine = pyttsx3.init()
engine.say("Jarvis is online!")
engine.runAndWait()

# Load memory
try:
    with open("memory.json", "r") as file:
        memory = json.load(file)
except FileNotFoundError:
    memory = {}

# Save memory function
def save_memory():
    with open("memory.json", "w") as file:
        json.dump(memory, file)

# Listening function
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return "I couldn't understand that"
        except sr.RequestError:
            return "API unavailable"

# Custom responses
custom_responses = {
    "who are you": "I am Jarvis, your virtual assistant!",
    "what can you do": "I can open apps, answer questions, and more!",
    "who made you": "I was created by Eshab Sachan!",
    "what's the weather like": "I'm not a weather bot, but I can find out if you want!",
    "who is anmol": "He is my own brother and a child of yours!",
    "open youtube": "Opening YouTube!",
    "open google": "Opening Google!",
    "shutdown computer": "Shutting down now!",
    "restart computer": "Restarting now!"
}

# Handle AI responses with G4F
def ask_jarvis(prompt):
    prompt = prompt.lower().strip()
    
    for question, answer in custom_responses.items():
        if question in prompt:
            return answer
    
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        return response
    except Exception as e:
        return f"Error: {e}"

# System stats function
def system_stats():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    battery = psutil.sensors_battery().percent
    return f"CPU: {cpu}% | RAM: {memory}% | Battery: {battery}%"

# Mood detection function
def detect_mood(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "happy"
    elif analysis.sentiment.polarity < 0:
        return "sad"
    else:
        return "neutral"

# File organizer function
def organize_files(directory):
    file_types = {'Images': ['.jpg', '.jpeg', '.png', '.gif'],
                  'Documents': ['.pdf', '.docx', '.txt'],
                  'Audio': ['.mp3', '.wav'],
                  'Videos': ['.mp4', '.mkv', '.avi'],
                  'Others': []}

    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        if os.path.isfile(filepath):
            moved = False
            for category, extensions in file_types.items():
                if any(file.endswith(ext) for ext in extensions):
                    folder = os.path.join(directory, category)
                    os.makedirs(folder, exist_ok=True)
                    os.rename(filepath, os.path.join(folder, file))
                    moved = True
                    break
            if not moved:
                folder = os.path.join(directory, 'Others')
                os.makedirs(folder, exist_ok=True)
                os.rename(filepath, os.path.join(folder, file))

# Handle commands
def handle_command(command):
    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "YouTube is now open!"

    if "open spotify" in command:
        webbrowser.open("https://open.spotify.com")
        return "Spotify is now open!"
    
    if "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Google is now open!"
    
    if "shutdown computer" in command:
        os.system("shutdown /s /t 1")
        return "Shutting down!"
    
    if "restart computer" in command:
        os.system("shutdown /r /t 1")
        return "Restarting!"
    
    if "system stats" in command:
        return system_stats()
    
    if "organize files" in command:
        organize_files(os.getcwd())
        return "Files organized!"
    
    return ask_jarvis(command)

# Main loop
def main():
    wake_word = "hey jarvis"
    while True:
        command = listen_command()

        if wake_word in command:
            engine.say("Yes, I'm here!")
            engine.runAndWait()

            while True:
                user_input = listen_command()
                
                if "stop" in user_input:
                    engine.say("Going offline!")
                    engine.runAndWait()
                    save_memory()
                    return
                
                mood = detect_mood(user_input)
                memory['last_mood'] = mood

                response = handle_command(user_input)
                print(f"Jarvis: {response}")
                engine.say(response)
                engine.runAndWait()

if __name__ == "__main__":
    main()
