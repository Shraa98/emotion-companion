"""
ML Service for loading models and making predictions.
Handles the lifecycle of the classic ML models.
"""

import os
import joblib
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "backend", "models")
SENTIMENT_MODEL_PATH = os.path.join(MODELS_DIR, "sentiment_model.joblib")
EMOTION_MODEL_PATH = os.path.join(MODELS_DIR, "emotion_model.joblib")

# Global variables to hold loaded models
_sentiment_model = None
_emotion_model = None

def load_models():
    """
    Load trained models from disk into memory.
    """
    global _sentiment_model, _emotion_model
    
    logger.info("Loading ML models...")
    
    # Load Sentiment Model
    if os.path.exists(SENTIMENT_MODEL_PATH):
        try:
            _sentiment_model = joblib.load(SENTIMENT_MODEL_PATH)
            logger.info("✅ Sentiment Model loaded.")
        except Exception as e:
            logger.error(f"Failed to load Sentiment Model: {e}")
            _sentiment_model = None
    else:
        logger.warning(f"⚠️ Sentiment Model not found at {SENTIMENT_MODEL_PATH}")
        _sentiment_model = None

    # Load Emotion Model
    if os.path.exists(EMOTION_MODEL_PATH):
        try:
            _emotion_model = joblib.load(EMOTION_MODEL_PATH)
            logger.info("✅ Emotion Model loaded.")
        except Exception as e:
            logger.error(f"Failed to load Emotion Model: {e}")
            _emotion_model = None
    else:
        logger.warning(f"⚠️ Emotion Model not found at {EMOTION_MODEL_PATH}")
        _emotion_model = None

def predict_sentiment(text: str) -> Dict[str, Any]:
    """
    Predict sentiment using the loaded Logistic Regression model.
    Returns: {label: "POSITIVE"/"NEGATIVE", score: float, confidence: float}
    """
    if not _sentiment_model:
        logger.warning("Sentiment model not loaded. Using fallback.")
        return {"label": "NEUTRAL", "score": 0.0, "confidence": 0.0}
    
    try:
        # Predict class
        prediction = _sentiment_model.predict([text])[0]
        # Predict probabilities
        probas = _sentiment_model.predict_proba([text])[0]
        confidence = max(probas)
        
        # Calculate score (-1 to 1) based on confidence and class
        # Assuming index 1 is POSITIVE, 0 is NEGATIVE (alphabetical order usually)
        # We need to check classes_ to be sure, but for now assuming standard binary
        classes = _sentiment_model.classes_
        pos_index = list(classes).index("POSITIVE") if "POSITIVE" in classes else 1
        
        pos_prob = probas[pos_index]
        neg_prob = 1 - pos_prob
        
        # Score: Map [0, 1] probability to [-1, 1] range
        score = (pos_prob - 0.5) * 2
        
        return {
            "label": prediction,
            "score": round(score, 3),
            "confidence": round(confidence, 3),
            "method": "logistic_regression"
        }
    except Exception as e:
        logger.error(f"Error predicting sentiment: {e}")
        return {"label": "NEUTRAL", "score": 0.0, "confidence": 0.0}

def predict_emotion(text: str) -> Dict[str, Any]:
    """
    Predict emotion using the loaded Naive Bayes model.
    Returns: {primary_emotion: str, emotion_scores: dict}
    """
    if not _emotion_model:
        logger.warning("Emotion model not loaded. Using fallback.")
        return {"primary_emotion": "neutral", "emotion_scores": {"neutral": 0.5}}
    
    try:
        # Predict class
        primary_emotion = _emotion_model.predict([text])[0]
        # Predict probabilities
        probas = _emotion_model.predict_proba([text])[0]
        classes = _emotion_model.classes_
        
        # Create scores dictionary
        emotion_scores = {cls: round(prob, 3) for cls, prob in zip(classes, probas)}
        
        return {
            "primary_emotion": primary_emotion,
            "emotion_scores": emotion_scores,
            "method": "naive_bayes"
        }
    except Exception as e:
        logger.error(f"Error predicting emotion: {e}")
        return {"primary_emotion": "neutral", "emotion_scores": {"neutral": 0.5}}

# Automatically load models on module import (but don't fail if missing)
load_models()
