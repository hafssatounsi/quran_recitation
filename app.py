import streamlit as st

# Manually install missing dependencies (for Streamlit Cloud)
try:
    import whisper
except ImportError:
    st.warning("Installing required packages, please wait...")
    import os
    os.system("pip install whisper numba llvmlite")
    import whisper  # Re-import after installation

import ollama
from gtts import gTTS
import torch
import numpy as np
import soundfile as sf
import io

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

    # Convert uploaded file to a NumPy array
    audio_bytes = uploaded_file.read()
    audio_buffer = io.BytesIO(audio_bytes)

    # Load audio using SoundFile
    audio_data, samplerate = sf.read(audio_buffer, dtype="float32")

    # Convert to Whisper-compatible NumPy format
    audio_tensor = torch.from_numpy(audio_data)

    # Transcribe the audio
    user_text = whisper_model.transcribe(audio_tensor.numpy())["text"].strip()
    
    st.write(f"**You said:** {user_text}")

    # Use Ollama to analyze mistakes
    feedback = analyze_mistake(user_text, correct_verse)

    speak(feedback)  # Provide correction in audio form
    st.write(feedback)
