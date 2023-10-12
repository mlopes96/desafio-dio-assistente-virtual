# import section
import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime
import playsound
import wikipedia
import webbrowser


# Get mic audio
def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio, language="en")
            print(said)
        except sr.UnknownValueError:
            speak("Sorry, I did not get that.")
        except sr.RequestError:
            speak("Sorry, the service is not available")
    return said.lower()


# Speak converted audio to text
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "voice.mp3"
    try:
        os.remove(filename)
    except OSError:
        pass
    tts.save(filename)
    playsound.playsound(filename)


# Function to respond to commands
def respond(text):
    print("Text from get audio " + text)
    if 'youtube' in text:
        speak("What do you want to search for?")
        keyword = get_audio()
        if keyword != '':
            url = f"https://www.youtube.com/results?search_query={keyword}"
            webbrowser.get().open(url)
            speak(f"Here is what I have found for {keyword} on youtube")
    elif 'search' in text:
        speak("What do you want to search for?")
        query = get_audio()
        if query != '':
            result = wikipedia.summary(query, sentences=3)
            speak("According to wikipedia")
            print(result)
            speak(result)
    elif 'what time' in text:
        str_time = datetime.today().strftime("%H:%M %p")
        print(str_time)
        speak(str_time)
    elif 'exit' in text:
        speak("Goodbye, till next time")
        exit()


# Start the virtual assistant
while True:
    speak("Starting assistant")
    print("I am listening...")
    text = get_audio()
    respond(text)
