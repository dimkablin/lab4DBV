# import modele that can convert voice to text
import json
import os

import pyttsx3, pyaudio, vosk
import requests

tts = pyttsx3.init()

voices = tts.getProperty('voices')
tts.setProperty('voices', 'ru')

for voice in voices:
    print(voice.name)
    if voice == "Microsoft Irina Desktop - Russian":
        tts.setProperty('voice', voice.id)


def say_something(text: str):
    tts.say(text)
    tts.runAndWait()


model = vosk.Model('model_small')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)

stream.start_stream()


def speak(say):
    tts.say(say)
    tts.runAndWait()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


pwd = None
for text in listen():
    if text == 'блокнот':
        os.system('notepad.exe')

    elif text == 'закрыть':
        quit()

    elif text == 'пароль':
        req = requests.get('https://passwordinator.onrender.com/?num=true')
        data = req.json()
        pwd = data['data']
        print(pwd)

    elif text == 'сохранить':
        if pwd:
            with open("result.txt", 'w') as file:
                file.write(pwd)
                print('recorded')
        else:
            print('nothing to recorded')
    else:
        print(text)

