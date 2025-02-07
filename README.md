# Quran Recitation Correction App

This application listens to Quran recitation, detects mistakes, and suggests pronunciation corrections using Whisper and Ollama LLM.

## How to Run
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   streamlit run app.py
   ```

## Deployment
This project is deployed using **Streamlit Cloud**.

## Features
✅ Uses **Whisper** for speech-to-text  
✅ Uses **Ollama LLM** for mistake detection & correction  
✅ Detects **2 minutes of silence** and helps the user  
✅ **Web-based app** using **Streamlit**  

## How It Works
1. The user starts reciting a Quranic verse.
2. The system listens using **Whisper ASR**.
3. The text is compared with the correct verse.
4. **Ollama LLM** detects mistakes and suggests pronunciation corrections.
5. If the user is silent for **2 minutes**, the system prompts them with the next word.

## Contribution
Feel free to contribute! Open a **Pull Request** with improvements or fixes.

## License
This project is open-source under the MIT License.
