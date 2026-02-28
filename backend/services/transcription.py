import os
from openai import OpenAI
from config import Config

# Initialize Groq Client
client = OpenAI(
    api_key=Config.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def transcribe_audio(file_path: str, dialect: str) -> str:
    """
    Transcribes audio using OpenAI Whisper.
    Uses prompt to enforce dialect and instruction to preserve repetitions for clinical analysis.
    """
    system_prompt = f"Transcribe Tamil speech accurately. Dialect: {dialect}. Preserve filler words and repetition for speech analysis. Do not normalize."
    
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-large-v3", 
                file=audio_file,
                prompt=system_prompt,
                response_format="text"
            )
        return transcript
    except Exception as e:
        print(f"Error in transcription: {e}")
        return "Transcription error fallback."
