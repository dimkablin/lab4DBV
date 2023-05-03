# import modele that can convert voice to text
import json
import os
from PIL import Image
import urllib.request

import pyttsx3, pyaudio, vosk
import requests


class MyBot:
    def __init__(self):
        self.picture = None
        self.success = False
        self.message = ""
        self.type_of_dog = ""
        self.id = ""

        self.tts = pyttsx3.init()

        voices = self.tts.getProperty('voices')
        self.tts.setProperty('voices', 'ru')

        for voice in voices:
            print(voice.name)
            if voice == "Microsoft Irina Desktop - Russian":
                self.tts.setProperty('voice', voice.id)

        self.model = vosk.Model('model_small')
        self.record = vosk.KaldiRecognizer(self.model, 16000)
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=pyaudio.paInt16,
                                   channels=1,
                                   rate=16000,
                                   input=True,
                                   frames_per_buffer=8000)

        self.stream.start_stream()

    def say_something(self, text: str):
        self.tts.say(text)
        self.tts.runAndWait()

    def speak(self, say):
        self.tts.say(say)
        self.tts.runAndWait()

    def listen(self):
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.record.AcceptWaveform(data) and len(data) > 0:
                answer = json.loads(self.record.Result())
                if answer['text']:
                    yield answer['text']

    def info(self):
        print(self.message,
              self.success)

    def start_listen(self):
        for text in self.listen():
            if text == 'блокнот':
                os.system('notepad.exe')

            elif text == 'закрыть':
                quit()

            elif text == 'картинка':
                req = requests.get('https://dog.ceo/api/breeds/image/random')
                data = req.json()
                self.success = data['status']
                if self.success:
                    self.message = data['message']
                    self.type_of_dog = self.message.split("/")[-2]
                    self.id = self.message.split("/")[-1]
                    urllib.request.urlretrieve(self.message, "picture_temp.png")
                    self.picture = Image.open("picture_temp.png")

            elif text == 'сохранить':
                if self.success:
                    self.picture.save("temp.png")
                    print('saved')
                else:
                    print('nothing to recorded')

            elif text == "покажи":
                if self.success:
                    self.picture.show()
                else:
                    self.say_something("Картинки нет")

            elif text == "тип":
                if self.success:
                    self.say_something(self.type_of_dog)
                    print(self.type_of_dog)

            elif text == "качество":
                if self.success:
                    print(self.picture.size)

            elif text == "информация":
                self.info()

            print('>', text)

    def test(self):
        req = requests.get('https://dog.ceo/api/breeds/image/random')
        data = req.json()
        self.success = data['status']
        if self.success:
            self.message = data['message']
            urllib.request.urlretrieve(self.message, "picture_temp.png")
            self.picture = Image.open("picture_temp.png")
            self.picture.show()


maBot = MyBot()
maBot.start_listen()

