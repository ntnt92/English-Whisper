import streamlit as st
import openai
import speech_recognition as sr
import pyaudio
import tempfile
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.title("🎙️ English Speech-to-Text & Text-to-Speech")

# Speech-to-Text Section
st.header("🎤 Speech to Text")

# Function to record audio using speech_recognition
def record_audio(duration=5):
    st.info("Recording... Speak now!")

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=duration)

    st.success("Recording complete!")

    # Save the audio to a temporary .wav file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        with open(tmp_wav.name, "wb") as f:
            f.write(audio.get_wav_data())
        return tmp_wav.name

# Option 1: Record Speech
if st.button("🎙️ Start Recording"):
    audio_path = record_audio()

    with open(audio_path, "rb") as audio:
        response = openai.Audio.transcribe("whisper-1", audio, language="en")
        transcript = response.get("text", "")

    os.remove(audio_path)  # Clean up temporary file
    st.text_area("📝 Transcribed Text:", transcript, height=150)

# Option 2: Upload Audio File
st.subheader("📤 Upload an English audio file (MP3, WAV)")
uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
        tmp_audio.write(uploaded_file.read())
        tmp_audio_path = tmp_audio.name

    st.audio(tmp_audio_path, format="audio/mp3")

    with open(tmp_audio_path, "rb") as audio:
        response = openai.Audio.transcribe("whisper-1", audio, language="en")
        transcript = response.get("text", "")

    os.remove(tmp_audio_path)  # Clean up temp file
    st.text_area("📝 Transcribed Text:", transcript, height=150)
