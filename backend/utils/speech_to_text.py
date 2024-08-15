import groq
import os

from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


client = groq.Groq(api_key=GROQ_API_KEY)
model = "whisper-large-v3"
temperature = 0.0
response_format = "json"

def transcribe_audio(audio_file_path,audio_file_name):

    with open(audio_file_path+audio_file_name, "rb") as file:
        result = client.audio.transcriptions.create(file=(audio_file_path+audio_file_name,file.read()), model=model, temperature=temperature, response_format=response_format)
        print(result.text)
        return result.text