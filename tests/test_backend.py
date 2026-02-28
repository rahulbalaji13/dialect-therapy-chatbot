import sys
import os
import pytest
from flask import Flask
from config import Config

# Add backend to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app import app, socketio

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.json == {"status": "healthy"}
    
def test_transcription_prompt():
    from services.transcription import transcribe_audio
    # Should use mocked/patched OpenAI client, but here we can just verify script fails gracefully if no key/audio
    assert transcribe_audio("fake_path.webm", "Kongu") == "Transcription error fallback."

def test_therapy_json_structure():
    from services.therapy import generate_therapy
    res = generate_therapy("sample", "Kongu", 0.5, ["Stutter"])
    assert "exercises" in res
    assert "feedback" in res

def test_impediment_scoring_mock():
    from services.scoring import score_impediment
    # Mocking a fallback behavior if audio fails to load properly with torch
    res = score_impediment("bad_file.mp3")
    assert res["severity"] in ["mild", "moderate", "severe"]
    assert "fluency_score" in res
