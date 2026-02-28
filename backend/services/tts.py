import base64
import os
import secrets
from gtts import gTTS

def text_to_speech_base64(text: str) -> str:
    """Generate TTS using free gTTS and return base64 audio"""
    try:
        tmp_file = f"tmp_audio/{secrets.token_hex(8)}_tts.mp3"
        
        # Free TTS generation
        tts = gTTS(text=text, lang='en', slow=False) 
        tts.save(tmp_file)
        
        with open(tmp_file, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode("utf-8")
            
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
            
        return audio_b64
    except Exception as e:
        print(f"Error in TTS generation: {e}")
        return ""
