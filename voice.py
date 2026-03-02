import pyttsx3
import speech_recognition as sr
import whisper
from config import VOICE_RATE, VOICE_VOLUME, WHISPER_MODEL

# ── Text to Speech Setup ──────────────────────────
engine = pyttsx3.init()
engine.setProperty('rate', VOICE_RATE)
engine.setProperty('volume', VOICE_VOLUME)

# Pick a voice — 0 is usually male, 1 is usually female on Windows
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    """SILAS speaks out loud"""
    print(f"SILAS: {text}")
    engine.say(text)
    engine.runAndWait()

# ── Speech Recognition Setup ─────────────────────
recognizer = sr.Recognizer()
recognizer.energy_threshold = 400
recognizer.dynamic_energy_threshold = True

# Load Whisper model once at startup
print("Loading Whisper model... please wait")
whisper_model = whisper.load_model(WHISPER_MODEL)
print("Whisper ready.")

def listen():
    """Listen through microphone and return text"""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing speech...")
            
            # Save audio temporarily and run through Whisper
            with open("temp_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            result = whisper_model.transcribe("temp_audio.wav")
            text = result["text"].strip()
            
            print(f"You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print(f"Listen error: {e}")
            return None