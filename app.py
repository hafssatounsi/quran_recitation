import streamlit as st
import whisper
import ollama
from gtts import gTTS
import os

# Load Whisper model
whisper_model = whisper.load_model("base")

# Sample Quranic verse
correct_verse = "Bismillah ir Rahman ir Rahim"

def speak(text):
    """Convert text to speech using gTTS."""
    tts = gTTS(text=text, lang="ar")
    tts.save("output.mp3")
    st.audio("output.mp3")  # Play audio in Streamlit

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

st.title("Quran Recitation Correction")

# File uploader instead of microphone
uploaded_file = st.file_uploader("Upload an audio file (MP3/WAV)", type=["mp3", "wav"])

if uploaded_file:
    st.write("Processing...")
    
    # Save the uploaded file
    with open("uploaded_audio.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Convert speech to text using Whisper
    user_text = whisper_model.transcribe("uploaded_audio.wav")["text"].strip()
    
    st.write(f"**You said:** {user_text}")

    # Use Ollama to analyze mistakes
    feedback = analyze_mistake(user_text, correct_verse)

    speak(feedback)  # Provide correction in audio form
    st.write(feedback)
