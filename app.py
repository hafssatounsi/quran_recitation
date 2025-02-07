import streamlit as st
import whisper
import ollama
from gtts import gTTS
import torch
import numpy as np
import soundfile as sf
import io

# Cache Whisper model for faster execution
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("tiny")  # Using "tiny" model for speed

whisper_model = load_whisper_model()

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
    The user recited: "{user_text}".
    The correct verse is: "{correct_text}".

    Compare and list only incorrect words and their corrections.
    No extra explanations, just the incorrect words with their fixed versions.
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
    user_text = whisper_model.transcribe(audio_tensor.numpy(), word_timestamps=False)["text"].strip()
    
    st.write(f"**You said:** {user_text}")
    
    # Use Ollama to analyze mistakes
    feedback = analyze_mistake(user_text, correct_verse)
    
    speak(feedback)  # Provide correction in audio form
    st.write(feedback)
