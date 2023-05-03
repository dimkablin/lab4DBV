# import modele that can convert voice to text
import pyttsx3

tts = pyttsx3.init()

voices = tts.getProperty('voices')
tts.setProperty('voices', 'en')

for voice in voices:
    print(voice.name)
    if voice == "Microsoft Zira Desktop - English (United States)":
        tts.setProperty('voice', voice.id)

tts.say("Hello")
tts.runAndWait()