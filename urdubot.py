
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv(".env")

# Configure the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key="Openai api key here")
st.write("""
# Urdu Voice Assistant App
## Made by **XYZ**
In this app users can give a voice input in اردو and it should process the input and respond in اردو language (text and audio).
""")

# Define a function to record voice input
def record_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Recording... Please speak in Urdu.")
        audio = r.listen(source)
    return audio

# Define a function to convert voice input to text
def voice_to_text(audio):
    try:
        recognizer = sr.Recognizer()
        text = recognizer.recognize_google(audio, language="ur-PK")
        return text
    except sr.UnknownValueError:
        st.error("Could not understand audio")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results; {e}")
        return None

# Define a function to generate a response using OpenAI's API
def generate_response(input_text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": input_text}
            ],
            max_tokens=250
        )

        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "معذرت، کچھ غلط ہو گیا ہے."  # "Sorry, something went wrong."

# Define a function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='ur')
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

# Define a function to play audio
def play_audio(audio_file):
    audio_segment = AudioSegment.from_file(audio_file, format="mp3")
    play(audio_segment)

# Create a button in the Streamlit app to trigger voice input
if st.button("Record Voice Input"):
    audio_input = record_voice()
    if audio_input:
        input_text = voice_to_text(audio_input)
        if input_text:
            st.write(f"Recognized Text: {input_text}")
            response_text = generate_response(input_text)
            st.write(f"Chatbot Response: {response_text}")

            audio_response = text_to_speech(response_text)
            st.audio(audio_response, format="audio/mp3")
            play_audio(audio_response)