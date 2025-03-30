import streamlit as st
import openai
import pyaudio
import wave
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

# Function to record audio using PyAudio
def record_audio(duration=5, samplerate=44100):
    st.info("Recording... Speak now!")

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    CHUNK = 1024  # Buffer size

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=samplerate, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(samplerate / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    st.success("Recording complete!")

    # Save recorded audio to a temporary .wav file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        with wave.open(tmp_wav.name, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(samplerate)
            wf.writeframes(b''.join(frames))
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
