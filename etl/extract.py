import whisper
import streamlit as st
import shutil

@st.cache_resource
def load_whisper():
    if shutil.which("ffmpeg") is None:
        st.error("FFMPEG NOT FOUND! Please install ffmpeg and restart. See instructions below.")
        st.stop()
    return whisper.load_model("small")

def transcribe_audio(audio_path):
    model = load_whisper()
    with st.spinner("Transcribing... This takes 2-5 mins for 1hr audio"):
        result = model.transcribe(audio_path, fp16=False)
    return result["text"], result["segments"]