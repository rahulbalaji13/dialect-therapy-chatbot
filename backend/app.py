import os
import secrets
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

from config import Config
from services.transcription import transcribe_audio
from services.scoring import score_impediment
from services.therapy import generate_therapy
from services.tts import text_to_speech_base64
from utils.supabase_client import supabase_client

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for frontend framework calls
CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}})

# WebSockets setup
# async_mode='eventlet' is standard for production, but using default 'threading' for robust local
socketio = SocketIO(app, cors_allowed_origins=Config.CORS_ORIGINS)

os.makedirs('tmp_audio', exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "message": "Welcome to Dialect Therapy Chatbot API!",
        "endpoints": ["/health", "/sessions", "/analyze", "/live-session"]
    }), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/sessions', methods=['GET'])
def get_sessions():
    """Fetch user sessions from Supabase"""
    user_id = request.args.get('user_id', 'guest')
    if not supabase_client:
        return jsonify({"data": [], "mock": True})
        
    try:
        response = supabase_client.table("sessions").select("*").eq("user_id", user_id).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    """
    Standard HTTP endpoint for processing a single recording
    Steps: Save file, Transcribe, Score, Therapy plan, Save to DB
    """
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
        
    audio_file = request.files['audio']
    dialect = request.form.get('dialect', 'Madurai')
    user_id = request.form.get('user_id', 'guest')
    
    file_path = f"tmp_audio/{secrets.token_hex(8)}.webm"
    audio_file.save(file_path)
    
    # Pipeline
    transcript = transcribe_audio(file_path, dialect)
    scoring = score_impediment(file_path)
    therapy = generate_therapy(transcript, dialect, scoring.get("fluency_score", 0), scoring.get("detected_patterns", []))
    
    # Store session info in DB
    session_data = {
        "user_id": user_id,
        "dialect": dialect,
        "transcript": transcript,
        "fluency_score": scoring.get("fluency_score"),
        "severity": scoring.get("severity"),
        "therapy_plan": therapy
    }
    
    if supabase_client:
        try:
            supabase_client.table("sessions").insert(session_data).execute()
        except Exception as e:
            print(f"Supabase error: {e}")
            
    # Cleanup temp audio
    if os.path.exists(file_path):
        os.remove(file_path)
        
    return jsonify({
        "success": True,
        "transcript": transcript,
        "scoring": scoring,
        "therapy": therapy
    })


@socketio.on('connect', namespace='/live-session')
def test_connect():
    emit('session_status', {'data': 'Connected to Live Session Therapy Loop'})

@socketio.on('audio_chunk', namespace='/live-session')
def handle_audio(data):
    """
    WebSocket endpoint for real-time therapy loop.
    Frontend sends binary audio chunks. We assemble them, transcribe, score, and push TTS back.
    """
    dialect = data.get('dialect', 'Kongu')
    audio_data = data.get('audio') # Bytes
    
    if not audio_data:
        emit('error', {'message': 'No audio data received'})
        return
        
    file_path = f"tmp_audio/live_{secrets.token_hex(8)}.webm"
    with open(file_path, "wb") as f:
        f.write(audio_data)
        
    emit('status_update', {'step': 'Transcribing...'})
    transcript = transcribe_audio(file_path, dialect)
    emit('transcript_live', {'text': transcript})
    
    emit('status_update', {'step': 'Analyzing Impeding Factors...'})
    scoring = score_impediment(file_path)
    emit('score_live', {'score': scoring})
    
    emit('status_update', {'step': 'Generating Therapy...'})
    therapy = generate_therapy(transcript, dialect, scoring.get("fluency_score", 0), scoring.get("detected_patterns", []))
    emit('therapy_live', {'therapy': therapy})
    
    emit('status_update', {'step': 'Synthesizing Voice...'})
    feedback_tts_b64 = text_to_speech_base64(therapy.get("feedback", ""))
    emit('audio_feedback', {'audio_b64': feedback_tts_b64})
    
    if os.path.exists(file_path):
        os.remove(file_path)

if __name__ == '__main__':
    # Start SocketIO server
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
