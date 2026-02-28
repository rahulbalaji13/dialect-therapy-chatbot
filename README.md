# Dialect Therapy Chatbot (Tamil Dialect AI Speech Therapy)

Dialect Therapy Chatbot is a production-ready multilingual speech-therapy web app designed for Tamil dialect speakers (Kongu, Madurai, Tirunelveli). It enables users to practice speech dynamically, receive real-time impediment analysis, and generate highly personalized dialect-specific therapies.

---

## 🚀 Features

- **Dialect-Aware Transcription**: Uses OpenAI Whisper with tailored system prompts to capture the nuances of Tamil dialects.
- **Impediment Detection**: Simulates acoustic and phonetic level feature extraction (e.g. paused speech rate, repetitions) using PyTorch architecture schemas and heuristics to provide an objective Fluency Score.
- **Generative AI Therapy**: Constructs 5 custom-tailored exercises based specifically on the user's transcript and score using GPT-4o-mini inside a rigid JSON structure format.
- **Voice Feedback Loop**: Converts the AI therapy back to speech (OpenAI TTS streamable base64).
- **Progress Analytics**: Tracks longitudinal speech progress week-over-week visualized via Chart.js on the Frontend.
- **WebSocket Streaming**: Near real-time looping between recording chunks and the AI processing pipeline.

## 🏗 System Architecture

- **Frontend**: Vue 3 (Composition API), Vite, TypeScript, Vuetify
- **Backend**: Python 3.11, Flask, Flask-SocketIO
- **Database**: Supabase (PostgreSQL), with native integration capabilities

Directory structure strictly splits into loosely coupled micro-components for edge deployment.

## 🛠 Local Setup Strategy

### Backend
1. `cd backend`
2. `python -m venv venv`
3. `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill the variables (OpenAI, Supabase)
6. Run `python app.py`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

## 🔒 Security Practices Configured
- `.env` pattern to prevent secrets leak.
- Socket Origin validation configured in the main loop backend `config.py`.
- No sensitive keys sent over standard JSON payload.

## 🎥 60-Second Demo Script

*(Camera opens on a sleek smartphone screen displaying a dark mode UI with a bright blue microphone icon glowing gently. The presenter hits "Record".)*

**NARRATOR (Voiceover):**
*"Speech therapy needs to speak your language. Not just Tamil... your region's Tamil. Welcome to the Dialect Therapy Chatbot."*

*(Presenter clicks a bold dropdown on the screen and selects "Madurai Dialect".)*

**NARRATOR (Voiceover):**
*"We start by picking a dialect. The AI tunes its microphone to capture every hesitation and colloquial cadence."*

*(Presenter dictates into the app while a real-time glowing animation dances on the screen. The transcription pops up instantly.)*

**NARRATOR (Voiceover):**
*"As you speak, our custom Whisper pipeline captures your voice exactly. We pass it directly into our underlying machine-learning models, simulating torchaudio representations, looking for underlying fluency gaps or stuttering."*

*(Within two seconds, an animated radial gauge sweeps to '68% Moderation Form' and a specific list 'High pause frequency' appears right below it.)*

**NARRATOR (Voiceover):**
*"You get an objective, real-time score. But we don't just score you—we treat you."*

*(The screen scrolls down seamlessly to a "Therapy Plan" tab. 3 AI-generated exercises matching the transcript's vocabulary populate alongside an upbeat audio response auto-playing from the screen.)*

**NARRATOR (Voiceover):**
*"In seconds, GPT-4 creates personalized repetitions, breathing plans, and a culturally relevant tongue twister targeting exactly what you struggled with."*

*(Screen transitions to the History tab flashing a brightly colored Chart.js graph trending consistently upward from 55% to 81% fluency)*

**NARRATOR (Voiceover):**
*"Every session is logged to Supabase to build longitudinal growth insights. This is therapy tailored, structured, and available anywhere."*

*(Fade out with the logo: 'Dialect Therapy Chatbot - Your speech, your rules.')*
