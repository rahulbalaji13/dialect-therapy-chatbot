import json
from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def generate_therapy(transcript: str, dialect: str, fluency_score: float, detected_patterns: list) -> dict:
    """
    Generate structured personalized therapy using GPT-4o-mini
    """
    prompt = f"""
    You are an expert AI speech therapist specializing in Tamil dialects.
    
    User Transcript: {transcript}
    Dialect: {dialect}
    Fluency Score: {fluency_score} (0 is severe, 1 is perfect)
    Detected Issues: {', '.join(detected_patterns)}
    
    Generate output in strictly this JSON format, no markdown wrapping, no extra text:
    {{
        "exercises": [
            {{"type": "repetition", "content": "Sentence 1 in dialect..."}},
            {{"type": "repetition", "content": "Sentence 2 in dialect..."}},
            {{"type": "repetition", "content": "Sentence 3 in dialect..."}},
            {{"type": "breathing", "content": "Step by step breathing control instruction..."}},
            {{"type": "tongue_twister", "content": "Culturally relevant tongue twister in dialect..."}}
        ],
        "feedback": "Encouraging, natural feedback in English or Tanglish..."
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Return only raw JSON based on the user's instructions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        data = response.choices[0].message.content
        return json.loads(data)
    except Exception as e:
        print(f"Error in therapy generation: {e}")
        return {
            "exercises": [],
            "feedback": "Error generating therapy plan."
        }
