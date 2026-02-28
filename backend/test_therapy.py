import os
from dotenv import load_dotenv
load_dotenv('backend/.env')
from openai import OpenAI
import json

client = OpenAI(
    api_key=os.environ.get('GROQ_API_KEY'),
    base_url='https://api.groq.com/openai/v1'
)

transcript = "எனக்கு மூன்று நாட்களாக வயிறு வலிக்கிறது என்ன செய்வது என்று கூறும்."
dialect = "Chennai"
fluency_score = 0.75
detected_patterns = ["Simulated: Mild pacing issues"]

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

print("Running prompt...")
try:
    response = client.chat.completions.create(
        model='llama3-8b-8192',
        messages=[
            {'role': 'system', 'content': 'You must output strictly raw JSON.'},
            {'role': 'user', 'content': prompt}
        ],
        temperature=0.7,
        response_format={'type': 'json_object'}
    )
    data = response.choices[0].message.content
    print("--- RAW DATA ---")
    print(data)
    
    if data.startswith("```json"):
        data = data.replace("```json", "", 1)
    if data.startswith("```"):
        data = data.replace("```", "", 1)
    if data.endswith("```"):
        data = data[::-1].replace("```", "", 1)[::-1]
        
    res = json.loads(data.strip())
    print("--- SUCCESS PARSING JSON! ---")
    print(res)
except Exception as e:
    print(f"--- ERROR ---")
    print(e)
