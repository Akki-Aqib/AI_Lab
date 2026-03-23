"""
Text to Speech (TTS) & Speech Recognition
Uses:
  - pyttsx3  → offline TTS (no API key needed)
  - SpeechRecognition → speech-to-text via Google Web Speech API
  
Install: pip install pyttsx3 SpeechRecognition pyaudio
"""

# ─── TEXT TO SPEECH ──────────────────────────────────────────────────
def text_to_speech_demo():
    try:
        import pyttsx3
        engine = pyttsx3.init()

        # List available voices
        voices = engine.getProperty('voices')
        print("Available Voices:")
        for i, voice in enumerate(voices):
            print(f"  [{i}] {voice.name} — {voice.id}")

        # Configure engine
        engine.setProperty('rate', 150)       # Speed (words per minute)
        engine.setProperty('volume', 1.0)     # Volume 0.0 to 1.0
        if voices:
            engine.setProperty('voice', voices[0].id)

        texts = [
            "Hello! Welcome to Artificial Intelligence Lab.",
            "Text to speech synthesis is working perfectly.",
            "This program converts text into spoken audio."
        ]
        for text in texts:
            print(f"\nSpeaking: \"{text}\"")
            engine.say(text)
            engine.runAndWait()

        # Save speech to file
        engine.save_to_file("Hello from Python Text to Speech!", "output_speech.mp3")
        engine.runAndWait()
        print("\nSpeech saved to output_speech.mp3")

    except ImportError:
        print("[TTS] pyttsx3 not installed. Run: pip install pyttsx3")
    except Exception as e:
        print(f"[TTS] Error: {e}")

# ─── SPEECH RECOGNITION ──────────────────────────────────────────────
def speech_recognition_demo():
    try:
        import speech_recognition as sr
        recognizer = sr.Recognizer()

        print("\n=== Speech Recognition Demo ===")
        # From microphone
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening... Speak now!")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        # Try multiple recognition engines
        print("Recognizing...")
        try:
            text = recognizer.recognize_google(audio)
            print(f"Google Speech API: \"{text}\"")
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Google API error: {e}")

        # From audio file
        print("\n--- Recognizing from audio file ---")
        try:
            with sr.AudioFile("output_speech.mp3") as source:
                audio_file = recognizer.record(source)
            text = recognizer.recognize_google(audio_file)
            print(f"Recognized from file: \"{text}\"")
        except Exception as e:
            print(f"File recognition error: {e}")

    except ImportError:
        print("[SR] SpeechRecognition not installed. Run: pip install SpeechRecognition pyaudio")
    except Exception as e:
        print(f"[SR] Error: {e}")

# ─── SIMULATION (no microphone needed) ───────────────────────────────
def simulate_tts_pipeline():
    print("=== Simulated TTS Pipeline (no hardware needed) ===\n")
    texts = [
        "Artificial Intelligence is transforming the world.",
        "Machine learning enables computers to learn from data.",
        "Natural language processing bridges humans and machines."
    ]
    for text in texts:
        words = text.split()
        print(f"Input text ({len(words)} words): \"{text}\"")
        audio_duration = len(words) / 2.5  # ~2.5 words/sec at 150wpm
        print(f"  → Estimated audio duration: {audio_duration:.1f} seconds")
        print(f"  → Characters processed: {len(text)}")
        print(f"  → Phonemes (estimated): {len(text) * 0.6:.0f}\n")

if __name__ == "__main__":
    print("=" * 50)
    print("   Text to Speech & Speech Recognition")
    print("=" * 50)
    simulate_tts_pipeline()
    print("\n[Live TTS — requires pyttsx3]")
    text_to_speech_demo()
    print("\n[Live ASR — requires microphone]")
    speech_recognition_demo()
