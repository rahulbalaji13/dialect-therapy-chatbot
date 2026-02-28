import torch
import random
import torchaudio
import numpy as np

# We provide a mock implementation architecture that represents how wav2vec2 extracts
# features. In production, an actual fine-tuned wav2vec2 local or via Inference API is used.

class MockImpedimentScorer:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.severity_levels = ["mild", "moderate", "severe"]

    def extract_features(self, waveform: torch.Tensor, sample_rate: int):
        """Simulates computing speech rate, pause frequency, pitch variance."""
        # Represents deep feature extraction
        duration = waveform.shape[1] / sample_rate
        # Fake features based on duration and random variance representing a processed wav2vec2 state
        speech_rate = max(0.5, random.gauss(3.0, 1.0)) # Words per second
        pause_freq = random.randint(0, int(duration / 2))
        repetition_freq = random.randint(0, 5)
        pitch_variance = random.uniform(0.1, 0.9)
        articulation_conf = random.uniform(0.5, 0.99)
        
        return {
            "speech_rate": speech_rate,
            "pause_frequency": pause_freq,
            "repetition_frequency": repetition_freq,
            "pitch_variance": pitch_variance,
            "articulation_confidence": articulation_conf
        }

    def predict(self, file_path: str):
        try:
            waveform, sample_rate = torchaudio.load(file_path)
            # Ensure mono
            if waveform.shape[0] > 1:
                waveform = torch.mean(waveform, dim=0, keepdim=True)
            
            features = self.extract_features(waveform, sample_rate)
            
            # Simple simulation of RNN/LSTM scoring layer -> 0-1 fluency score
            # A higher speech rate and articulation, with fewer pauses/repetitions => ~1.0
            
            fluency_score = min(1.0, max(0.0, (
                features['articulation_confidence'] * 0.4 + 
                (1.0 / (1.0 + features['pause_frequency'])) * 0.3 + 
                (1.0 / (1.0 + features['repetition_frequency'])) * 0.3
            )))
            
            if fluency_score > 0.8: severity = "mild"
            elif fluency_score > 0.5: severity = "moderate"
            else: severity = "severe"
            
            patterns = []
            if features['pause_frequency'] > 3: patterns.append("High pause frequency")
            if features['repetition_frequency'] > 2: patterns.append("Stuttering repetitions")
            if features['speech_rate'] < 1.5: patterns.append("Slow speech rate / dysarthria")
            if not patterns: patterns.append("Normal fluency variation")
            
            return {
                "fluency_score": round(fluency_score, 2),
                "severity": severity,
                "detected_patterns": patterns,
                "raw_features": features
            }
        except Exception as e:
            print(f"Error in predicting score: {e}")
            # Fallback mock for testing or demo without local ffmpeg/sox
            return {
                "fluency_score": 0.75,
                "severity": "mild",
                "detected_patterns": ["Simulated: Mild pacing issues"],
                "raw_features": {}
            }

scorer = MockImpedimentScorer()

def score_impediment(audio_file_path: str) -> dict:
    return scorer.predict(audio_file_path)
