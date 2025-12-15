"""
Pydantic models for request/response validation.
Defines the data structures used in API endpoints.
"""

from pydantic import BaseModel, Field, UUID4
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============================================================================
# User Models
# ============================================================================

class UserCreate(BaseModel):
    """Request model for creating a new user."""
    email: str = Field(..., description="User email address")
    name: Optional[str] = Field(None, description="User full name")


class UserResponse(BaseModel):
    """Response model for user data."""
    id: UUID4
    email: str
    name: Optional[str]
    created_at: datetime


# ============================================================================
# Analysis Result Models
# ============================================================================

class SentimentResult(BaseModel):
    """Sentiment analysis result."""
    label: str = Field(..., description="POSITIVE, NEGATIVE, or NEUTRAL")
    score: float = Field(..., description="Confidence score between -1 and 1")


class EmotionResult(BaseModel):
    """Emotion detection result."""
    primary_emotion: str = Field(..., description="Primary detected emotion")
    emotion_scores: Dict[str, float] = Field(..., description="All emotion scores")
    emoji: str = Field(..., description="Emoji representing the emotion")


class AnalysisResult(BaseModel):
    """Complete analysis result for a journal entry."""
    sentiment: SentimentResult
    emotion: EmotionResult
    mood_score: int = Field(..., ge=0, le=10, description="Mood score from 0-10")
    themes: List[str] = Field(..., description="Extracted themes/keywords")
    highlighted_phrases: Dict[str, List[str]] = Field(
        ...,
        description="Phrases that contributed to each emotion/theme"
    )
    suggestions: List[str] = Field(..., description="Coping suggestions")
    metadata: Optional[Dict[str, Any]] = None


# ============================================================================
# Journal Entry Models
# ============================================================================

class JournalEntryCreate(BaseModel):
    """Request model for creating a journal entry."""
    user_id: UUID4 = Field(..., description="User ID")
    text: str = Field(..., min_length=10, description="Journal entry text")


class JournalEntryResponse(BaseModel):
    """Response model for journal entry with analysis."""
    id: UUID4
    user_id: UUID4
    text: str
    mood_score: Optional[int]
    sentiment: Optional[float]
    sentiment_label: Optional[str]
    emotion: Optional[str]
    emotion_scores: Optional[Dict[str, Any]]
    themes: Optional[List[str]]
    metadata: Optional[Dict[str, Any]]
    highlighted_phrases: Optional[Dict[str, Any]]
    suggestions: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
    
    # Include full analysis in response
    analysis: Optional[AnalysisResult] = None


class JournalEntryList(BaseModel):
    """Response model for list of journal entries."""
    entries: List[JournalEntryResponse]
    total: int
    page: int
    page_size: int


# ============================================================================
# Audio Entry Models
# ============================================================================

class AudioUploadResponse(BaseModel):
    """Response model for audio upload."""
    id: UUID4
    user_id: UUID4
    file_path: str
    file_name: Optional[str]
    transcript: Optional[str]
    transcription_status: str
    analysis: Optional[AnalysisResult] = None
    created_at: datetime


# ============================================================================
# Health Check Model
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    database: str
    nlp_models: Dict[str, bool]
