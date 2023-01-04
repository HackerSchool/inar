# from .emotion import Emotion
# from .phrase import Phrase

from vosk import Model, KaldiRecognizer
import pyaudio
import json

def captureAudio():
    model = Model(r"./vosk-model-small-en-us-0.15") 
    recognizer = KaldiRecognizer(model,  16000) #TODO: search the frequency and the class

    # Recognize from microphone
    capture = pyaudio.PyAudio()
    stream = capture.open(format= pyaudio.paInt16, channels=1, rate= 16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    return Audio(stream, recognizer)


class Audio():
    
    def __init__(self, stream, recognizer) -> None:
        self.stream = stream
        self.recognizer = recognizer

    # def emotionFromAudio(self) -> Emotion:
    #     """
    #     Extracts the emotion from a voice.
    #     """
    #     emotion = Emotion.NEUTRAL
    #     # TODO: implement this
    #     return emotion

    def phraseFromAudio(self):
        """
        Extracts the phrase from a voice.
        """
        text = ""

        while True:
            data = self.stream.read(4096)
            if self.recognizer.AcceptWaveform(data):
                #https://github.com/alphacep/vosk-api/blob/master/python/test/transcribe_scp.py
                res = json.loads(self.recognizer.Result()) 
                #text += " " + res["text"]
                text = res["text"]
                print(text)

        #phrase = Phrase.UNKNOWN
        # TODO: stop at end of x time or at bye/stop instruction

        #return phrase


# def main():
#     audio = captureAudio()

#     audio.phraseFromAudio()

# main()