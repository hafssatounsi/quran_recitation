import streamlit as st
import speech_recognition as sr
import ollama
import whisper
import time
from gtts import gTTS
import os

# Load Whisper model
whisper_model = whisper.load_model("base")

# Sample Quranic verse
correct_verse = "Bismillah ir Rahman ir Rahim"

# Speech recognition setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    """Convert text to speech using gTTS."""
    tts = gTTS(text=text, lang="ar")  # Use Arabic language
    tts.save("output.mp3")  # Save to a file
    os.system("mpg321 output.mp3")  # Play the file (on local system)

def analyze_mistake(user_text, correct_text):
    """Use Ollama LLM to analyze mistakes and suggest corrections."""
    prompt = f"""
    The user is reciting the Quran. They said: "{user_text}".
    The correct verse is: "{correct_text}".
    
    1. Identify any mistakes.
    2. Suggest the correct pronunciation for a beginner.
    3. Provide a simple explanation to improve.
    """

    response = ollama.chat(model="llama2", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def listen_and_correct():
    """Main function to listen to user recitation and provide corrections."""
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        last_speech_time = time.time()

        while True:
            try:
                st.write("Listening...")
                audio = recognizer.listen(source, timeout=120)

                # Convert speech to text using Whisper
                user_text = whisper_model.transcribe(audio)["text"].strip()
                last_speech_time = time.time()

                st.write(f"You said: {user_text}")

                # Use Ollama to analyze mistakes
                feedback = analyze_mistake(user_text, correct_verse)

                speak(feedback)  # Use gTTS instead of pyttsx3
                st.write(feedback)

            except sr.UnknownValueError:
                st.write("Could not understand audio, please try again.")
            except sr.RequestError:
                st.write("Speech Recognition service is unavailable.")
            except sr.WaitTimeoutError:
                if time.time() - last_speech_time > 120:
                    speak("Need help? The next word is: " + correct_verse.split()[0])
                    last_speech_time = time.time()

# Streamlit UI
st.title("Quran Recitation Correction")
if st.button("Start Reciting"):
    listen_and_correct()
