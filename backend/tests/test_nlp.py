"""
Unit tests for NLP module.
Tests preprocessing, sentiment analysis, emotion detection, and theme extraction.
"""

import pytest
from backend.nlp import (
    preprocess,
    sentiment,
    emotion,
    extract_themes,
    calculate_mood_score,
    generate_suggestions,
    analyze_text
)


class TestPreprocessing:
    """Test text preprocessing functions."""
    
    def test_preprocess_lowercase(self):
        """Test that text is converted to lowercase."""
        text = "I Feel AMAZING Today!"
        result = preprocess(text)
        assert result == "i feel amazing today!"
    
    def test_preprocess_whitespace(self):
        """Test that extra whitespace is removed."""
        text = "I   feel    great"
        result = preprocess(text)
        assert result == "i feel great"


class TestSentiment:
    """Test sentiment analysis."""
    
    def test_sentiment_positive(self):
        """Test positive sentiment detection."""
        text = "I am so happy and excited about this wonderful day!"
        result = sentiment(text)
        
        assert "label" in result
        assert "score" in result
        assert result["label"] in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
        assert -1 <= result["score"] <= 1
    
    def test_sentiment_negative(self):
        """Test negative sentiment detection."""
        text = "I feel terrible and sad. Everything is going wrong."
        result = sentiment(text)
        
        assert "label" in result
        assert result["label"] in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    
    def test_sentiment_neutral(self):
        """Test neutral sentiment detection."""
        text = "I went to the store today."
        result = sentiment(text)
        
        assert "label" in result
        assert "score" in result


class TestEmotion:
    """Test emotion detection."""
    
    def test_emotion_detection(self):
        """Test that emotion detection returns expected structure."""
        text = "I am feeling very anxious and worried about tomorrow."
        result = emotion(text)
        
        assert "primary_emotion" in result
        assert "emotion_scores" in result
        assert "emoji" in result
        assert isinstance(result["emotion_scores"], dict)
    
    def test_emotion_happy(self):
        """Test happy emotion detection."""
        text = "I am so happy and joyful! This is amazing!"
        result = emotion(text)
        
        # Should detect some positive emotion
        assert result["primary_emotion"] in ["happy", "joy", "excited"]


class TestThemeExtraction:
    """Test theme extraction."""
    
    def test_extract_themes(self):
        """Test that themes are extracted from text."""
        text = """
        I had a difficult day at work today. My boss was very demanding
        and I felt overwhelmed by all the projects. I need to find better
        work-life balance.
        """
        themes = extract_themes(text)
        
        assert isinstance(themes, list)
        assert len(themes) > 0
        # Should extract work-related themes
        assert any("work" in theme.lower() or "project" in theme.lower() for theme in themes)


class TestMoodScore:
    """Test mood score calculation."""
    
    def test_mood_score_positive(self):
        """Test mood score for positive sentiment."""
        score = calculate_mood_score(sentiment_score=0.8, emotion_intensity=0.7)
        assert 0 <= score <= 10
        assert score > 5  # Should be in upper half
    
    def test_mood_score_negative(self):
        """Test mood score for negative sentiment."""
        score = calculate_mood_score(sentiment_score=-0.8, emotion_intensity=0.7)
        assert 0 <= score <= 10
        assert score < 5  # Should be in lower half
    
    def test_mood_score_neutral(self):
        """Test mood score for neutral sentiment."""
        score = calculate_mood_score(sentiment_score=0.0, emotion_intensity=0.3)
        assert 0 <= score <= 10
        assert 4 <= score <= 6  # Should be near middle


class TestSuggestions:
    """Test coping suggestions generation."""
    
    def test_generate_suggestions(self):
        """Test that suggestions are generated."""
        suggestions = generate_suggestions("anxious", ["work", "deadline"])
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        assert all(isinstance(s, str) for s in suggestions)


class TestAnalyzeText:
    """Test complete text analysis."""
    
    def test_analyze_text_complete(self):
        """Test that complete analysis returns all expected fields."""
        text = "I feel really anxious about my work presentation tomorrow."
        result = analyze_text(text)
        
        # Check all required fields are present
        assert "sentiment" in result
        assert "emotion" in result
        assert "mood_score" in result
        assert "themes" in result
        assert "suggestions" in result
        assert "highlighted_phrases" in result
        assert "metadata" in result
        
        # Check types
        assert isinstance(result["sentiment"], dict)
        assert isinstance(result["emotion"], dict)
        assert isinstance(result["mood_score"], int)
        assert isinstance(result["themes"], list)
        assert isinstance(result["suggestions"], list)
    
    def test_analyze_text_positive(self):
        """Test analysis of positive text."""
        text = "I am so happy and grateful for this wonderful day!"
        result = analyze_text(text)
        
        assert result["sentiment"]["label"] == "POSITIVE"
        assert result["mood_score"] >= 5
    
    def test_analyze_text_negative(self):
        """Test analysis of negative text."""
        text = "I feel terrible and everything is going wrong."
        result = analyze_text(text)
        
        assert result["sentiment"]["label"] == "NEGATIVE"
        assert result["mood_score"] <= 5
