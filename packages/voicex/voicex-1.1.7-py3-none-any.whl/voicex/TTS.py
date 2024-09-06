import requests
from io import BytesIO
import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd
import pickle
import webbrowser
import sys
import enum


class TTS():
    def __init__(self, voice=None, server=None, port="5000", ssl=False):
        if server is None:
            sys.exit("VoiceX: You have to specify the TTS server IP/URL!!!")

        self.server = server
        self.port = port
        if not ssl:
            protocol = "http://"
        else:
            protocol = "https://"
        self.base_url = protocol + self.server + ":" + self.port
        self.endpoint = self.base_url + "/api"
        if voice is None:
            self.open_web_interface()
        else:
            if isinstance(voice, enum.Enum):
                voice_path = voice.value
            else:
                voice_path = voice
            with open(voice_path, 'rb') as inp:
                self.voice = dict(enumerate(pickle.load(inp)))
    def synthesize(self, text):
        json_dict = self.voice
        json_dict["text"] = text
        res = requests.post(self.endpoint, json=json_dict)
        if res.ok:
            response_bytes = BytesIO(res.content)
            header = response_bytes.read(44)  # Assuming a standard WAV header size of 44 bytes
            sample_rate = int.from_bytes(header[24:28], byteorder='little')
            wav_data = np.frombuffer(response_bytes.read(), dtype=np.int16)
            return wav_data, sample_rate
        else:
            print("Something went wrong with the TTS API call.")
            return None, None

    def speak(self, text):
        wav_data, sample_rate = self.synthesize(text)
        sd.play(wav_data, sample_rate)
        sd.wait()

    def write(self, text, filename):
        wav_data, sample_rate = self.synthesize(text)
        write(filename, sample_rate, wav_data)

    def open_web_interface(self):
        webbrowser.open(self.base_url)
        sys.exit("VoiceX: Build a voice file.")