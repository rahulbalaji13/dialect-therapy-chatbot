from openai import OpenAI
from config import Config
import base64

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def text_to_speech_base64(text: str) -> str:
    """Generate TTS and return base64 audio to stream through websockets or HTTP"""
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy", # or nova
            input=text,
            response_format="mp3"
        )
        return base64.b64encode(response.content).decode("utf-8")
    except Exception as e:
        print(f"Error in TTS generation: {e}")
        return ""
