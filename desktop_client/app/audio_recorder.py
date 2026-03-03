import base64
import wave
from io import BytesIO
import numpy as np
import sounddevice as sd

class AudioRecorder:
    def __init__(self, samplerate=16000):
        self.samplerate = samplerate

    def record_wav_b64(self, seconds: float = 2.5) -> str:
        frames = int(self.samplerate * seconds)
        audio = sd.rec(frames, samplerate=self.samplerate, channels=1, dtype="int16")
        sd.wait()
        pcm = audio.tobytes()

        bio = BytesIO()
        with wave.open(bio, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # int16
            wf.setframerate(self.samplerate)
            wf.writeframes(pcm)

        return base64.b64encode(bio.getvalue()).decode("utf-8")