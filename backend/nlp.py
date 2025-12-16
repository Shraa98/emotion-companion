"""
NLP (Natural Language Processing) module for emotional analysis.
Provides sentiment analysis, emotion detection, theme extraction, and coping suggestions.

REFACTORED: Uses Classic ML models (Logistic Regression, Naive Bayes) via ml_service.
"""

import re
import logging
from typing import Dict, List, Any
import json
import os

# NLP Libraries
try:
    import spacy
except Exception as e:
    logging.getLogger(__name__).warning(f"Failed to import spacy: {e}")
    spacy = None
from rake_nltk import Rake

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import ML Service (Classic ML)
from backend.ml_service import predict_sentiment, predict_emotion

# Load configuration
from backend.config import settings

# ============================================================================
# Model Initialization
# ============================================================================

# Initialize spaCy for preprocessing/lemmatization
if spacy:
    try:
        nlp_spacy = spacy.load("en_core_web_sm")
    except OSError:
        logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
        nlp_spacy = None
    except Exception as e:
        logger.warning(f"Error loading spaCy: {e}")
        nlp_spacy = None
else:
    nlp_spacy = None


# ============================================================================
# Text Preprocessing
# ============================================================================

def preprocess(text: str) -> str:
    """
    Preprocess text for NLP analysis.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


# ============================================================================
# Theme Extraction
# ============================================================================

def extract_themes(text: str, top_n: int = 5) -> List[str]:
    """
    Extract main themes/keywords from text using RAKE.
    """
    try:
        rake = Rake()
        rake.extract_keywords_from_text(text)
        ranked = rake.get_ranked_phrases()
        themes = [t for t in ranked if len(t) > 3]
        return themes[:top_n]
    
    except Exception as e:
        logger.error(f"Theme extraction error: {e}")
        words = text.lower().split()
        common = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "is", "am", "are"}
        return [w for w in list(set(words)) if w not in common and len(w) > 3][:top_n]


# ============================================================================
# Mood Score Calculation
# ============================================================================

def calculate_mood_score(sentiment_score: float, emotion_intensity: float) -> int:
    """
    Calculate overall mood score from 0 (very negative) to 10 (very positive).
    """
    # Map sentiment from [-1, 1] to [0, 10]
    base_score = (sentiment_score + 1) * 5
    
    # Adjust by emotion intensity
    if sentiment_score > 0:
        adjusted_score = base_score + (emotion_intensity * 2)
    else:
        adjusted_score = base_score - (emotion_intensity * 2)
    
    return int(max(0, min(10, round(adjusted_score))))


# ============================================================================
# Coping Suggestions
# ============================================================================

def generate_suggestions(primary_emotion: str, themes: List[str]) -> List[str]:
    """
    Generate personalized coping suggestions based on emotion and themes.
    """
    emoji_map = load_emoji_map()
    
    # Get base suggestions
    emotion_data = emoji_map.get(primary_emotion, {})
    # Fallback to neutral if emotion not found
    if not emotion_data:
         emotion_data = emoji_map.get("neutral", {})
         
    base_suggestions = emotion_data.get("suggestions", [
        "Take a few deep breaths",
        "Write down your thoughts",
        "Talk to someone you trust"
    ])
    
    # Add theme-specific suggestions (Simple rule-based)
    theme_suggestions = []
    text_themes = " ".join(themes).lower()
    
    if any(k in text_themes for k in ["work", "job", "career", "boss", "project"]):
        theme_suggestions.append("Consider taking a short break from work tasks")
    if any(k in text_themes for k in ["friend", "family", "partner", "love"]):
        theme_suggestions.append("Reach out to someone you care about")
    if any(k in text_themes for k in ["school", "exam", "study", "grade"]):
        theme_suggestions.append("Remember that one test doesn't define you")

    return (base_suggestions + theme_suggestions)[:5]


# ============================================================================
# Main Analysis Function
# ============================================================================

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Perform complete emotional analysis on text.
    Uses Classic ML Models (Logistic Regression, Naive Bayes).
    """
    cleaned_text = preprocess(text)
    
    # 1. Sentiment Analysis (Logistic Regression)
    sentiment_result = predict_sentiment(cleaned_text)
    
    # 2. Emotion Detection (Naive Bayes)
    emotion_result = predict_emotion(cleaned_text)
    
    # Inject Emoji (Required by API Model)
    emoji_map = load_emoji_map()
    primary_emo = emotion_result.get("primary_emotion", "neutral")
    emotion_data = emoji_map.get(primary_emo, emoji_map.get("neutral", {}))
    emotion_result["emoji"] = emotion_data.get("emoji", "😐")
    
    # 3. Theme Extraction (RAKE)
    themes = extract_themes(text)
    
    # 4. Mood Score (Rule-Based)
    # Estimate intensity from confidence if available, else 0.5
    try:
        # Get max score from emotion_scores dict
        emotion_intensity = max(emotion_result["emotion_scores"].values())
    except:
        emotion_intensity = 0.5
        
    mood_score = calculate_mood_score(sentiment_result["score"], emotion_intensity)
    
    # 5. Suggestions
    suggestions = generate_suggestions(emotion_result["primary_emotion"], themes)
    
    # 6. Phrase Highlighting
    highlighted_phrases = {}
    for theme in themes:
        pattern = re.compile(r'\b' + re.escape(theme) + r'\b', re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            highlighted_phrases[theme] = matches[:3]
    
    return {
        "sentiment": sentiment_result,
        "emotion": emotion_result,
        "mood_score": mood_score,
        "themes": themes,
        "highlighted_phrases": highlighted_phrases,
        "suggestions": suggestions,
        "metadata": {
            "text_length": len(text),
            "word_count": len(text.split()),
            "models_used": {
                "sentiment": sentiment_result.get("method"),
                "emotion": emotion_result.get("method")
            }
        }
    }


# ============================================================================
# Utility Functions
# ============================================================================

def load_emoji_map() -> Dict[str, Any]:
    """
    Load emotion-to-emoji mapping.
    """
    try:
        emoji_path = os.path.join("utils", "emoji_map.json")
        if os.path.exists(emoji_path):
            with open(emoji_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Could not load emoji map: {e}")
    
    return {
        "happy": {"emoji": "😊", "suggestions": ["Celebrate this positive moment!", "Share your joy."]},
        "sad": {"emoji": "😢", "suggestions": ["It's okay to feel sad.", "Reach out to a friend."]},
        "angry": {"emoji": "😠", "suggestions": ["Take deep breaths.", "Go for a walk."]},
        "anxious": {"emoji": "😰", "suggestions": ["Focus on what you can control.", "Practice grounding."]},
        "fear": {"emoji": "😨", "suggestions": ["You are safe right now.", "Talk to someone."]},
        "surprise": {"emoji": "😲", "suggestions": ["Take a moment to process.", "Write about it."]},
        "neutral": {"emoji": "😐", "suggestions": ["Check in with yourself.", "Practice mindfulness."]},
        "calm": {"emoji": "😌", "suggestions": ["Enjoy the peace.", "Practice gratitude."]}
    }
