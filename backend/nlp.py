"""
NLP (Natural Language Processing) module for emotional analysis.
Provides sentiment analysis, emotion detection, theme extraction, and coping suggestions.

This module supports both HuggingFace transformer models and lightweight fallback methods
for environments without GPU or model dependencies.
"""

import re
import logging
from typing import Dict, List, Any, Tuple
import json
import os

# NLP Libraries
try:
    import spacy
except Exception as e:
    logging.getLogger(__name__).warning(f"Failed to import spacy: {e}")
    spacy = None
from sklearn.feature_extraction.text import TfidfVectorizer
from rake_nltk import Rake

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
from backend.config import settings

# ============================================================================
# Model Initialization
# ============================================================================

# Initialize spaCy for preprocessing
# Initialize spaCy for preprocessing
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

# Initialize HuggingFace models if enabled
sentiment_pipeline = None
emotion_pipeline = None

if settings.use_hf_models:
    try:
        from transformers import pipeline
        
        # Sentiment analysis model (lightweight DistilBERT)
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=-1  # CPU
        )
        logger.info("Loaded HuggingFace sentiment model")
        
        # Emotion detection model (optional, lightweight RoBERTa)
        try:
            emotion_pipeline = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=None,  # Return all emotion scores
                device=-1  # CPU
            )
            logger.info("Loaded HuggingFace emotion model")
        except Exception as e:
            logger.warning(f"Could not load emotion model: {e}. Using fallback.")
            emotion_pipeline = None
            
    except Exception as e:
        logger.warning(f"Could not load HuggingFace models: {e}. Using fallback methods.")
        sentiment_pipeline = None
        emotion_pipeline = None

# Initialize VADER for fallback sentiment analysis
vader_analyzer = None
if not sentiment_pipeline:
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer
        import nltk
        # Download VADER lexicon if not present
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon', quiet=True)
        vader_analyzer = SentimentIntensityAnalyzer()
        logger.info("Using VADER for sentiment analysis (fallback)")
    except Exception as e:
        logger.error(f"Could not initialize VADER: {e}")


# ============================================================================
# Emotion Keywords for Fallback
# ============================================================================

EMOTION_KEYWORDS = {
    "happy": ["happy", "joy", "excited", "great", "wonderful", "amazing", "fantastic", 
              "delighted", "cheerful", "pleased", "glad", "content", "thrilled"],
    "sad": ["sad", "unhappy", "depressed", "down", "miserable", "gloomy", "sorrowful",
            "heartbroken", "disappointed", "upset", "blue", "melancholy"],
    "angry": ["angry", "mad", "furious", "irritated", "annoyed", "frustrated", "rage",
              "outraged", "hostile", "resentful", "bitter"],
    "anxious": ["anxious", "worried", "nervous", "stressed", "tense", "uneasy", "fearful",
                "concerned", "apprehensive", "restless", "panic"],
    "fear": ["afraid", "scared", "terrified", "frightened", "alarmed", "horrified",
             "threatened", "intimidated", "dread"],
    "calm": ["calm", "peaceful", "relaxed", "serene", "tranquil", "composed", "balanced",
             "centered", "quiet", "still"],
    "surprise": ["surprised", "shocked", "astonished", "amazed", "startled", "stunned",
                 "unexpected", "sudden"]
}


# ============================================================================
# Text Preprocessing
# ============================================================================

def preprocess(text: str) -> str:
    """
    Preprocess text for NLP analysis.
    
    Steps:
    1. Convert to lowercase
    2. Remove extra whitespace
    3. Basic cleaning (keep punctuation for sentiment)
    
    Args:
        text: Raw input text
        
    Returns:
        Cleaned text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def lemmatize_text(text: str) -> str:
    """
    Lemmatize text using spaCy.
    Reduces words to their base form (e.g., "running" -> "run").
    
    Args:
        text: Input text
        
    Returns:
        Lemmatized text
    """
    if not nlp_spacy:
        return text
    
    doc = nlp_spacy(text)
    lemmatized = " ".join([token.lemma_ for token in doc if not token.is_stop])
    return lemmatized


# ============================================================================
# Sentiment Analysis
# ============================================================================

def sentiment(text: str) -> Dict[str, Any]:
    """
    Analyze sentiment of text.
    
    Uses HuggingFace DistilBERT model if available, otherwise falls back to VADER.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with:
        - label: "POSITIVE", "NEGATIVE", or "NEUTRAL"
        - score: Float between -1 (very negative) and 1 (very positive)
        - method: "huggingface" or "vader"
    """
    if sentiment_pipeline:
        # Use HuggingFace model
        try:
            result = sentiment_pipeline(text[:512])[0]  # Limit to 512 tokens
            label = result["label"]
            confidence = result["score"]
            
            # Convert to -1 to 1 scale
            if label == "POSITIVE":
                score = confidence
            else:  # NEGATIVE
                score = -confidence
            
            return {
                "label": label,
                "score": round(score, 3),
                "confidence": round(confidence, 3),
                "method": "huggingface"
            }
        except Exception as e:
            logger.error(f"HuggingFace sentiment error: {e}")
    
    # Fallback to VADER
    if vader_analyzer:
        try:
            scores = vader_analyzer.polarity_scores(text)
            compound = scores["compound"]
            
            # Determine label based on compound score
            if compound >= 0.05:
                label = "POSITIVE"
            elif compound <= -0.05:
                label = "NEGATIVE"
            else:
                label = "NEUTRAL"
            
            return {
                "label": label,
                "score": round(compound, 3),
                "confidence": round(abs(compound), 3),
                "method": "vader"
            }
        except Exception as e:
            logger.error(f"VADER sentiment error: {e}")
    
    # Ultimate fallback: neutral
    return {
        "label": "NEUTRAL",
        "score": 0.0,
        "confidence": 0.0,
        "method": "fallback"
    }


# ============================================================================
# Emotion Detection
# ============================================================================

def emotion(text: str) -> Dict[str, Any]:
    """
    Detect emotions in text.
    
    Uses HuggingFace emotion model if available, otherwise uses keyword matching.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with:
        - primary_emotion: Main detected emotion
        - emotion_scores: Dict of all emotion scores
        - emoji: Emoji representing the emotion
        - method: "huggingface" or "keywords"
    """
    # Load emoji mapping
    emoji_map = load_emoji_map()
    
    if emotion_pipeline:
        # Use HuggingFace emotion model
        try:
            results = emotion_pipeline(text[:512])[0]
            
            # Convert to dict
            emotion_scores = {item["label"]: round(item["score"], 3) for item in results}
            
            # Get primary emotion
            primary = max(emotion_scores.items(), key=lambda x: x[1])
            primary_emotion = primary[0]
            
            return {
                "primary_emotion": primary_emotion,
                "emotion_scores": emotion_scores,
                "emoji": emoji_map.get(primary_emotion, {}).get("emoji", "😐"),
                "method": "huggingface"
            }
        except Exception as e:
            logger.error(f"HuggingFace emotion error: {e}")
    
    # Fallback: keyword-based emotion detection
    text_lower = text.lower()
    emotion_scores = {}
    
    for emotion_name, keywords in EMOTION_KEYWORDS.items():
        # Count keyword matches
        count = sum(1 for keyword in keywords if keyword in text_lower)
        # Normalize by text length (words)
        word_count = len(text_lower.split())
        score = count / max(word_count, 1) * 10  # Scale up for visibility
        emotion_scores[emotion_name] = round(min(score, 1.0), 3)
    
    # Get primary emotion
    if emotion_scores:
        primary_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
    else:
        primary_emotion = "neutral"
        emotion_scores["neutral"] = 0.5
    
    return {
        "primary_emotion": primary_emotion,
        "emotion_scores": emotion_scores,
        "emoji": emoji_map.get(primary_emotion, {}).get("emoji", "😐"),
        "method": "keywords"
    }


# ============================================================================
# Theme Extraction
# ============================================================================

def extract_themes(text: str, top_n: int = 5) -> List[str]:
    """
    Extract main themes/keywords from text.
    
    Uses RAKE (Rapid Automatic Keyword Extraction) algorithm.
    
    Args:
        text: Input text
        top_n: Number of top themes to return
        
    Returns:
        List of theme strings
    """
    try:
        # Use RAKE for keyword extraction
        rake = Rake()
        rake.extract_keywords_from_text(text)
        
        # Get ranked phrases
        ranked = rake.get_ranked_phrases()
        
        # Return top N themes
        themes = ranked[:top_n]
        
        # Clean up themes (remove very short ones)
        themes = [t for t in themes if len(t) > 3]
        
        return themes[:top_n]
    
    except Exception as e:
        logger.error(f"Theme extraction error: {e}")
        
        # Fallback: simple word frequency
        words = text.lower().split()
        # Remove common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"}
        words = [w for w in words if w not in common_words and len(w) > 3]
        
        # Get unique words
        unique_words = list(set(words))[:top_n]
        return unique_words


# ============================================================================
# Mood Score Calculation
# ============================================================================

def calculate_mood_score(sentiment_score: float, emotion_intensity: float) -> int:
    """
    Calculate overall mood score from 0 (very negative) to 10 (very positive).
    
    Formula:
    - Base score from sentiment (-1 to 1 mapped to 0 to 10)
    - Adjusted by emotion intensity
    
    Args:
        sentiment_score: Sentiment score from -1 to 1
        emotion_intensity: Emotion intensity from 0 to 1
        
    Returns:
        Mood score from 0 to 10
    """
    # Map sentiment from [-1, 1] to [0, 10]
    base_score = (sentiment_score + 1) * 5
    
    # Adjust by emotion intensity (higher intensity = more extreme score)
    if sentiment_score > 0:
        # Positive sentiment: intensity pushes score higher
        adjusted_score = base_score + (emotion_intensity * 2)
    else:
        # Negative sentiment: intensity pushes score lower
        adjusted_score = base_score - (emotion_intensity * 2)
    
    # Clamp to 0-10 range
    mood_score = int(max(0, min(10, round(adjusted_score))))
    
    return mood_score


# ============================================================================
# Coping Suggestions
# ============================================================================

def generate_suggestions(primary_emotion: str, themes: List[str]) -> List[str]:
    """
    Generate personalized coping suggestions based on emotion and themes.
    
    Args:
        primary_emotion: Primary detected emotion
        themes: Extracted themes from text
        
    Returns:
        List of suggestion strings
    """
    emoji_map = load_emoji_map()
    
    # Get base suggestions for the emotion
    emotion_data = emoji_map.get(primary_emotion, {})
    base_suggestions = emotion_data.get("suggestions", [
        "Take a few deep breaths",
        "Write down your thoughts",
        "Talk to someone you trust"
    ])
    
    # Add theme-specific suggestions
    theme_suggestions = []
    
    # Check for work/career themes
    work_keywords = ["work", "job", "career", "boss", "colleague", "project"]
    if any(keyword in " ".join(themes).lower() for keyword in work_keywords):
        theme_suggestions.append("Consider taking a short break from work tasks")
    
    # Check for relationship themes
    relationship_keywords = ["friend", "family", "partner", "relationship", "love"]
    if any(keyword in " ".join(themes).lower() for keyword in relationship_keywords):
        theme_suggestions.append("Reach out to someone you care about")
    
    # Combine suggestions (limit to 5 total)
    all_suggestions = base_suggestions + theme_suggestions
    return all_suggestions[:5]


# ============================================================================
# Main Analysis Function
# ============================================================================

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Perform complete emotional analysis on text.
    
    This is the main entry point that combines all analysis functions.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Complete analysis results including sentiment, emotion, themes, and suggestions
    """
    # Preprocess text
    cleaned_text = preprocess(text)
    
    # Sentiment analysis
    sentiment_result = sentiment(cleaned_text)
    
    # Emotion detection
    emotion_result = emotion(cleaned_text)
    
    # Theme extraction
    themes = extract_themes(text)  # Use original text for better theme extraction
    
    # Calculate mood score
    emotion_intensity = max(emotion_result["emotion_scores"].values())
    mood_score = calculate_mood_score(sentiment_result["score"], emotion_intensity)
    
    # Generate suggestions
    suggestions = generate_suggestions(emotion_result["primary_emotion"], themes)
    
    # Highlight phrases (simplified - find theme keywords in text)
    highlighted_phrases = {}
    for theme in themes:
        # Find occurrences of theme keywords in original text
        pattern = re.compile(r'\b' + re.escape(theme) + r'\b', re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            highlighted_phrases[theme] = matches[:3]
    
    # Compile complete analysis
    analysis = {
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
    
    return analysis


# ============================================================================
# Utility Functions
# ============================================================================

def load_emoji_map() -> Dict[str, Any]:
    """
    Load emotion-to-emoji mapping from JSON file.
    
    Returns:
        Dictionary mapping emotions to emojis and suggestions
    """
    try:
        emoji_path = os.path.join("utils", "emoji_map.json")
        if os.path.exists(emoji_path):
            with open(emoji_path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.warning(f"Could not load emoji map: {e}")
    
    # Fallback emoji map
    return {
        "happy": {
            "emoji": "😊",
            "suggestions": [
                "Celebrate this positive moment!",
                "Share your joy with someone",
                "Write down what made you happy"
            ]
        },
        "sad": {
            "emoji": "😢",
            "suggestions": [
                "It's okay to feel sad. Be gentle with yourself",
                "Try some deep breathing exercises",
                "Reach out to a friend or loved one"
            ]
        },
        "angry": {
            "emoji": "😠",
            "suggestions": [
                "Take 10 deep breaths before reacting",
                "Go for a walk to cool down",
                "Write down what's making you angry"
            ]
        },
        "anxious": {
            "emoji": "😰",
            "suggestions": [
                "Practice the 5-4-3-2-1 grounding technique",
                "Focus on what you can control",
                "Try progressive muscle relaxation"
            ]
        },
        "fear": {
            "emoji": "😨",
            "suggestions": [
                "Remind yourself that you are safe right now",
                "Talk to someone you trust",
                "Practice deep breathing"
            ]
        },
        "calm": {
            "emoji": "😌",
            "suggestions": [
                "Enjoy this peaceful moment",
                "Practice gratitude",
                "Maintain your current routine"
            ]
        },
        "surprise": {
            "emoji": "😲",
            "suggestions": [
                "Take a moment to process this",
                "Write about how you feel",
                "Talk it through with someone"
            ]
        },
        "neutral": {
            "emoji": "😐",
            "suggestions": [
                "Check in with yourself regularly",
                "Try journaling about your day",
                "Practice mindfulness"
            ]
        }
    }
