"""
FastAPI application for Emotion Companion backend.
Provides REST API endpoints for journal entries, audio uploads, and emotional analysis.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
from uuid import UUID
import logging
from pathlib import Path

from backend.config import settings
from backend.models import (
    JournalEntryCreate,
    JournalEntryResponse,
    AudioUploadResponse,
    HealthResponse
)
from backend.crud import (
    create_journal_entry,
    get_journal_entries,
    get_journal_entry,
    create_audio_entry,
    count_user_entries
)
from backend.nlp import analyze_text
from backend.audio import process_audio_upload, is_supported_audio_format

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

# Mount static files for auth page
auth_dir = Path(__file__).parent.parent / "auth"
app.mount("/auth/static", StaticFiles(directory=str(auth_dir)), name="auth_static")


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Root endpoint - API welcome page.
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Emotion Companion API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }
            h1 {
                color: #667eea;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            .status {
                display: inline-block;
                background: #10b981;
                color: white;
                padding: 8px 16px;
                border-radius: 20px;
                font-weight: 600;
                margin-bottom: 30px;
            }
            .endpoints {
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
            }
            .endpoints h2 {
                color: #333;
                margin-bottom: 15px;
                font-size: 1.3em;
            }
            .endpoint {
                background: white;
                padding: 12px 16px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                transition: transform 0.2s;
            }
            .endpoint:hover {
                transform: translateX(5px);
            }
            .endpoint a {
                color: #667eea;
                text-decoration: none;
                font-weight: 500;
            }
            .endpoint a:hover {
                text-decoration: underline;
            }
            .endpoint-desc {
                color: #666;
                font-size: 0.9em;
                margin-top: 4px;
            }
            .footer {
                text-align: center;
                margin-top: 30px;
                color: #666;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 Emotion Companion API</h1>
            <p class="subtitle">AI-powered journal and mood reflection platform</p>
            <span class="status">✓ API Running</span>
            
            <div class="endpoints">
                <h2>📚 API Documentation</h2>
                <div class="endpoint">
                    <a href="/api/docs" target="_blank">/api/docs</a>
                    <div class="endpoint-desc">Interactive API documentation (Swagger UI)</div>
                </div>
                <div class="endpoint">
                    <a href="/api/redoc" target="_blank">/api/redoc</a>
                    <div class="endpoint-desc">Alternative API documentation (ReDoc)</div>
                </div>
            </div>

            <div class="endpoints">
                <h2>🔍 Health Checks</h2>
                <div class="endpoint">
                    <a href="/healthz" target="_blank">/healthz</a>
                    <div class="endpoint-desc">Simple health check</div>
                </div>
                <div class="endpoint">
                    <a href="/api/health" target="_blank">/api/health</a>
                    <div class="endpoint-desc">Detailed system status</div>
                </div>
            </div>

            <div class="endpoints">
                <h2>🔐 Authentication</h2>
                <div class="endpoint">
                    <a href="/auth" target="_blank">/auth</a>
                    <div class="endpoint-desc">User authentication page</div>
                </div>
            </div>

            <div class="footer">
                Version 1.0.0 • Powered by FastAPI
            </div>
        </div>
    </body>
    </html>
    """


# ============================================================================
# Authentication Page Route
# ============================================================================

@app.get("/auth", response_class=HTMLResponse)
async def serve_auth_page():
    """
    Serve the standalone HTML authentication page.
    """
    auth_html_path = Path(__file__).parent.parent / "auth" / "index.html"
    with open(auth_html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/auth/{filename}")
async def serve_auth_files(filename: str):
    """
    Serve CSS/JS files for auth page.
    """
    auth_file_path = Path(__file__).parent.parent / "auth" / filename
    if auth_file_path.exists():
        return FileResponse(auth_file_path)
    raise HTTPException(status_code=404, detail="File not found")

# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.get("/healthz")
def health():
    """Simple health check endpoint for monitoring services."""
    return {"status": "ok"}


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns API status and available NLP models.
    """
    # Check which NLP models are available
    from backend import nlp
    from backend.ml_service import _sentiment_model, _emotion_model
    
    models_available = {
        "sentiment_model": _sentiment_model is not None,
        "emotion_model": _emotion_model is not None,
        "spacy": nlp.nlp_spacy is not None
    }
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected",
        "nlp_models": models_available
    }


# ============================================================================
# Journal Entry Endpoints
# ============================================================================

@app.post("/api/journal/", response_model=JournalEntryResponse)
async def create_journal(entry: JournalEntryCreate):
    """
    Create a new journal entry with emotional analysis.
    
    This endpoint:
    1. Receives journal text from user
    2. Performs NLP analysis (sentiment, emotion, themes)
    3. Generates coping suggestions
    4. Saves entry to database
    5. Returns complete analysis results
    """
    try:
        # Perform NLP analysis
        logger.info(f"Analyzing journal entry for user {entry.user_id}")
        analysis = analyze_text(entry.text)
        
        # Save to database
        db_entry = create_journal_entry(
            user_id=entry.user_id,
            text=entry.text,
            analysis=analysis
        )
        
        if not db_entry:
            raise HTTPException(status_code=500, detail="Failed to save journal entry")
        
        # Add analysis to response
        db_entry["analysis"] = analysis
        
        return db_entry
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected server error")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@app.get("/api/journal/", response_model=List[JournalEntryResponse])
async def list_journal_entries(
    user_id: UUID = Query(..., description="User ID"),
    limit: int = Query(50, ge=1, le=100, description="Maximum entries to return"),
    offset: int = Query(0, ge=0, description="Number of entries to skip")
):
    """
    Get journal entries for a user with pagination.
    
    Query parameters:
    - user_id: User UUID (required)
    - limit: Max entries per page (default: 50, max: 100)
    - offset: Number of entries to skip (default: 0)
    """
    try:
        entries = get_journal_entries(user_id, limit, offset)
        return entries
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected server error")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@app.get("/api/journal/{entry_id}", response_model=JournalEntryResponse)
async def get_journal(entry_id: UUID):
    """
    Get a single journal entry by ID.
    """
    try:
        entry = get_journal_entry(entry_id)
        
        if not entry:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        
        return entry
        
    except HTTPException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected server error")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


# ============================================================================
# Audio Upload Endpoint
# ============================================================================

@app.post("/api/audio/", response_model=AudioUploadResponse)
async def upload_audio(
    user_id: UUID = Query(..., description="User ID"),
    file: UploadFile = File(..., description="Audio file")
):
    """
    Upload audio journal entry.
    
    This endpoint:
    1. Validates audio file format
    2. Uploads to Supabase Storage (or saves locally)
    3. Transcribes audio to text using Whisper
    4. Performs emotional analysis on transcript
    5. Saves to database
    6. Returns transcript and analysis
    
    Supported formats: MP3, WAV, M4A, OGG, FLAC
    """
    try:
        # Validate file format
        if not is_supported_audio_format(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported audio format. Supported: MP3, WAV, M4A, OGG, FLAC"
            )
        
        # Read file content
        file_bytes = await file.read()
        file_size = len(file_bytes)
        
        # Process upload and transcription
        logger.info(f"Processing audio upload for user {user_id}")
        file_path, transcript = process_audio_upload(
            file_bytes,
            file.filename,
            str(user_id)
        )
        
        if not file_path:
            raise HTTPException(status_code=500, detail="Failed to save audio file")
        
        # Analyze transcript if available
        analysis = None
        if transcript:
            logger.info("Analyzing audio transcript")
            analysis = analyze_text(transcript)
        
        # Save to database
        db_entry = create_audio_entry(
            user_id=user_id,
            file_path=file_path,
            file_name=file.filename,
            file_size=file_size,
            transcript=transcript,
            analysis=analysis
        )
        
        if not db_entry:
            raise HTTPException(status_code=500, detail="Failed to save audio entry")
        
        # Add analysis to response
        db_entry["analysis"] = analysis
        
        return db_entry
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected server error")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


# ============================================================================
# Application Lifecycle
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Starting Emotion Companion API")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Using Classic ML models")
    logger.info(f"Audio enabled: {settings.enable_audio}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down Emotion Companion API")
    
    # Close database connections
    # from backend.db import db
    # db.close_pool()
    logger.info("Supabase connection does not require explicit shutdown")


# ============================================================================
# Run Application
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
