# from .emotion import Emotion
# from .phrase import Phrase

from vosk import Model, KaldiRecognizer

import pyaudio
import json

import signal
import sys


class Audio():
    
    def __init__(self):
        self.model = Model("../../data/vosk-model-small-en-us-0.15") 
        self.recognizer = KaldiRecognizer(self.model,  16000)
        self.stream = pyaudio.PyAudio().open(format= pyaudio.paInt16, channels=1, rate= 16000, input=True, frames_per_buffer=8192)
        self.stream.start_stream()

    # def emotionFromAudio(self) -> Emotion:
    #     """
    #     Extracts the emotion from a voice.
    #     """
    #     emotion = Emotion.NEUTRAL
    #     # TODO: implement this
    #     return emotion

    def phraseFromAudio(self):
        """
        Extracts the phrase from the audio.
        """
        phrase = ""
        while True:
            try:
                data = self.stream.read(4096)
                if self.recognizer.AcceptWaveform(data):
                    res = json.loads(self.recognizer.Result())
                    phrase = res["text"]
                    print(phrase)
            except KeyboardInterrupt:
                break

        return phrase


audio = Audio()
audio.phraseFromAudio()
