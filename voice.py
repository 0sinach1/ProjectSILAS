import whisper
import sounddevice as sd
import numpy as np
import pyttsx3
from config import VOICE_RATE, VOICE_VOLUME, WHISPER_MODEL

# ── Text to Speech Setup ──────────────────────────
engine = pyttsx3.init()
engine.setProperty('rate', VOICE_RATE)
engine.setProperty('volume', VOICE_VOLUME)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    """SILAS speaks out loud"""
    print(f"SILAS: {text}")
    engine.say(text)
    engine.runAndWait()

# ── Whisper Setup ─────────────────────────────────
print("Loading Whisper model... please wait")
whisper_model = whisper.load_model(WHISPER_MODEL)
print("Whisper ready.")

# ── Recording Settings ────────────────────────────
SAMPLE_RATE = 16000
DURATION = 7

def listen():
    """Record audio from mic and transcribe with Whisper"""
    try:
        print("Listening...")

        audio = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='float32'
        )
        sd.wait()

        audio_data = np.squeeze(audio)

        print("Processing speech...")
        result = whisper_model.transcribe(
            audio_data,
            fp16=False,
            language="en"
        )
        text = result["text"].strip()

        if text:
            print(f"You said: {text}")
            return text
        else:
            return None

    except Exception as e:
        print(f"Listen error: {e}")
        return None