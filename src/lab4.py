# import modele that can convert voice to text
import pyttsx3

tts = pyttsx3.init()

voices = tts.getProperty('voices')
tts.setProperty('voices', 'ru')

for voice in voices:
    print(voice.name)
    if voice == "Microsoft Irina Desktop - Russian":
        tts.setProperty('voice', voice.id)

tts.say("Привет")
tts.runAndWait()