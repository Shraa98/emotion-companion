"""
Simplified backend app that works without database for testing NLP functionality.
This version delays database connection until actually needed.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from uuid import UUID
import logging

from backend.config import settings
from backend.models import (
    JournalEntryCreate,
    HealthResponse
)
from backend.nlp import analyze_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# FastAPI Application Setup
# ============================================================================

app = FastAPI(
    title="Emotion Companion API",
    description="AI-powered journal and mood reflection coach",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns API status and available NLP models.
    """
    # Check which NLP models are available
    from backend import nlp
    
    models_available = {
        "sentiment_hf": nlp.sentiment_pipeline is not None,
        "emotion_hf": nlp.emotion_pipeline is not None,
        "vader": nlp.vader_analyzer is not None,
        "spacy": nlp.nlp_spacy is not None
    }
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "not connected (test mode)",
        "nlp_models": models_available
    }


# ============================================================================
# Journal Entry Endpoint (No Database)
# ============================================================================

@app.post("/api/journal/analyze")
async def analyze_journal(entry: JournalEntryCreate):
    """
    Analyze journal entry without saving to database.
    Returns emotional analysis results with enhanced suggestions.
    """
    try:
        # Perform NLP analysis
        logger.info(f"Analyzing journal entry for user {entry.user_id}")
        analysis = analyze_text(entry.text)
        
        # Get enhanced personalized suggestions
        from backend.suggestions import generate_personalized_suggestions
        
        emotion = analysis.get("emotion", {}).get("primary_emotion", "neutral")
        mood_score = analysis.get("mood_score", 5)
        emotion_confidence = max(analysis.get("emotion", {}).get("emotion_scores", {}).values(), default=0.5)
        
        enhanced_suggestions = generate_personalized_suggestions(
            emotion=emotion,
            mood_score=mood_score,
            text=entry.text,
            emotion_confidence=emotion_confidence
        )
        
        # Replace basic suggestions with enhanced ones
        analysis["suggestions"] = enhanced_suggestions["suggestions"]
        analysis["life_domain"] = enhanced_suggestions["domain"]
        analysis["emotion_intensity"] = enhanced_suggestions["intensity"]
        
        if enhanced_suggestions.get("crisis_resources"):
            analysis["crisis_resources"] = enhanced_suggestions["crisis_resources"]
        
        # Return analysis without saving
        return {
            "user_id": str(entry.user_id),
            "text": entry.text,
            "analysis": analysis,
            "note": "Analysis complete. Database not connected - entry not saved."
        }
        
    except Exception as e:
        logger.error(f"Error analyzing journal entry: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Application Lifecycle
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Starting Emotion Companion API (Test Mode - No Database)")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Using HF models: {settings.use_hf_models}")
    logger.info("⚠️  Database connection disabled for testing")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down Emotion Companion API")


# ============================================================================
# Run Application
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.app_no_db:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
