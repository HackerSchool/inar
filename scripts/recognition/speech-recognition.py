from vosk import Model, KaldiRecognizer
import pyaudio
import json

model = Model(r"./vosk-model-small-en-us-0.15") 
recognizer = KaldiRecognizer(model,  16000) #TODO: search the frequency and the class

# Recognize from microphone

capture = pyaudio.PyAudio()
stream = capture.open(format= pyaudio.paInt16, channels=1, rate= 16000, input=True, frames_per_buffer=8192)
stream.start_stream()

text = ""

while True:
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        #https://github.com/alphacep/vosk-api/blob/master/python/test/transcribe_scp.py
        res = json.loads(recognizer.Result()) 
        text += " " + res["text"]
        #text = res["text"]
        print(text)