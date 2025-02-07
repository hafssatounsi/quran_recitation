import speech_recognition as sr
import pyttsx3
import time
import ollama
import whisper  # Install with `pip install openai-whisper`

# Initialize text-to-speech engine
tts = pyttsx3.init()

# Load Whisper model (use 'tiny' or 'base' for fast performance)
whisper_model = whisper.load_model("base")

# Quranic verse to compare against
correct_verse = "Bismillah ir Rahman ir Rahim"

# Speech recognition setup
recognizer = sr.Recognizer()
mic = sr.Microphone()

def speak(text):
    """Convert text to speech."""
    tts.say(text)
    tts.runAndWait()

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
        last_speech_time = time.time()  # Track silence

        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=120)
                
                # Convert speech to text using Whisper
                user_text = whisper_model.transcribe(audio)["text"].strip()
                last_speech_time = time.time()

                print(f"You said: {user_text}")

                # Use Ollama to analyze mistakes
                feedback = analyze_mistake(user_text, correct_verse)

                speak(feedback)
                print(feedback)

            except sr.UnknownValueError:
                print("Could not understand audio, please try again.")
            except sr.RequestError:
                print("Speech Recognition service is unavailable.")
            except sr.WaitTimeoutError:
                # Detect 2 minutes of silence
                if time.time() - last_speech_time > 120:
                    speak("Need help? The next word is: " + correct_verse.split()[0])
                    last_speech_time = time.time()

if __name__ == "__main__":
    speak("Start reciting the Quran.")
    listen_and_correct()
