"""
Standalone script to train and save classic ML models.
Run this script once to generate the .joblib model files.
"""

import os
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import training data
try:
    from backend.data.training_data import SENTIMENT_DATA, EMOTION_DATA
except ImportError:
    # Handle running as script from root
    import sys
    sys.path.append(os.getcwd())
    from backend.data.training_data import SENTIMENT_DATA, EMOTION_DATA

# Configuration
MODELS_DIR = os.path.join("backend", "models")

def train_and_save_models():
    """
    Train Logistic Regression (Sentiment) and Naive Bayes (Emotion) models.
    Save them to the models directory.
    """
    # Create models directory if not exists
    os.makedirs(MODELS_DIR, exist_ok=True)
    logger.info(f"Models directory: {MODELS_DIR}")

    # ==========================================
    # 1. Train Sentiment Model (Logic Regression)
    # ==========================================
    logger.info("Training Sentiment Model (Logistic Regression)...")
    
    # Prepare data
    X_sentiment = [text for text, label in SENTIMENT_DATA]
    y_sentiment = [label for text, label in SENTIMENT_DATA]
    
    # Create Pipeline
    sentiment_model = Pipeline([
        ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english')),
        ('clf', LogisticRegression(random_state=42))
    ])
    
    # Train
    sentiment_model.fit(X_sentiment, y_sentiment)
    logger.info(f"Sentiment Model trained on {len(X_sentiment)} samples.")
    
    # Save
    sentiment_path = os.path.join(MODELS_DIR, "sentiment_model.joblib")
    joblib.dump(sentiment_model, sentiment_path)
    logger.info(f"Saved Sentiment Model to: {sentiment_path}")

    # ==========================================
    # 2. Train Emotion Model (Naive Bayes)
    # ==========================================
    logger.info("Training Emotion Model (Naive Bayes)...")
    
    # Prepare data
    X_emotion = [text for text, label in EMOTION_DATA]
    y_emotion = [label for text, label in EMOTION_DATA]
    
    # Create Pipeline
    emotion_model = Pipeline([
        ('tfidf', TfidfVectorizer(lowercase=True, stop_words='english')),
        ('clf', MultinomialNB())
    ])
    
    # Train
    emotion_model.fit(X_emotion, y_emotion)
    logger.info(f"Emotion Model trained on {len(X_emotion)} samples.")
    
    # Save
    emotion_path = os.path.join(MODELS_DIR, "emotion_model.joblib")
    joblib.dump(emotion_model, emotion_path)
    logger.info(f"Saved Emotion Model to: {emotion_path}")
    
    logger.info("✅ All models trained and saved successfully!")

if __name__ == "__main__":
    train_and_save_models()
