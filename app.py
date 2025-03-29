import streamlit as st
import openai
import sounddevice as sd
import numpy as np
import tempfile
import os
import wave
from dotenv import load_dotenv


load_dotenv()
# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("🎙️ English Speech-to-Text & Text-to-Speech")

# Speech-to-Text Section
st.header("🎤 Speech to Text")

# Function to record audio
def record_audio(duration=5, samplerate=44100):
    st.info("Recording... Speak now!")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    st.success("Recording complete!")

    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        with wave.open(tmp_wav.name, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
        return tmp_wav.name

# Option 1: Record Speech
if st.button("🎙️ Start Recording"):
    audio_path = record_audio()

    with open(audio_path, "rb") as audio:
        response = openai.Audio.transcribe("whisper-1", audio, language="en")
        transcript = response.get("text", "")

    os.remove(audio_path)  # Clean up
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
