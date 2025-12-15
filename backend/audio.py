"""
Audio processing module for handling audio uploads and transcription.
Supports Supabase Storage for file storage and Whisper for transcription.
"""

import os
import logging
from typing import Optional, Tuple
from datetime import datetime

from backend.config import settings

logger = logging.getLogger(__name__)

# ============================================================================
# Supabase Storage Integration
# ============================================================================

def upload_to_supabase(
    file_bytes: bytes,
    file_name: str,
    user_id: str
) -> Optional[str]:
    """
    Upload audio file to Supabase Storage.
    
    Args:
        file_bytes: Audio file content as bytes
        file_name: Original filename
        user_id: User ID for organizing files
        
    Returns:
        File path in storage, or None if upload failed
    """
    try:
        from backend.supabase_client import get_supabase
        
        # Initialize Supabase client
        supabase = get_supabase()
        
        # Create unique file path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"{user_id}/{timestamp}_{file_name}"
        
        # Upload to storage bucket
        response = supabase.storage.from_(settings.storage_bucket).upload(
            path=file_path,
            file=file_bytes,
            file_options={"content-type": "audio/mpeg"}
        )
        
        logger.info(f"Uploaded audio file to Supabase: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Error uploading to Supabase Storage: {e}")
        return None


def save_audio_locally(
    file_bytes: bytes,
    file_name: str,
    user_id: str
) -> Optional[str]:
    """
    Save audio file locally (fallback if Supabase not configured).
    
    Args:
        file_bytes: Audio file content as bytes
        file_name: Original filename
        user_id: User ID for organizing files
        
    Returns:
        Local file path, or None if save failed
    """
    try:
        # Create uploads directory
        upload_dir = os.path.join("uploads", "audio", user_id)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(upload_dir, f"{timestamp}_{file_name}")
        
        # Write file
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        
        logger.info(f"Saved audio file locally: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Error saving audio locally: {e}")
        return None


# ============================================================================
# Audio Transcription
# ============================================================================

def transcribe_audio(file_path: str) -> Optional[str]:
    """
    Transcribe audio file to text using Whisper.
    
    Supports both:
    1. OpenAI Whisper API (if API key configured)
    2. Local Whisper model (if installed)
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Transcribed text, or None if transcription failed
    """
    if not settings.enable_audio:
        logger.info("Audio transcription is disabled in settings")
        return None
    
    # Try OpenAI Whisper API first
    if settings.openai_api_key:
        try:
            import openai
            openai.api_key = settings.openai_api_key
            
            with open(file_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file
                )
            
            logger.info("Transcribed audio using OpenAI Whisper API")
            return transcript["text"]
            
        except Exception as e:
            logger.error(f"OpenAI Whisper API error: {e}")
    
    # Try local Whisper model
    try:
        import whisper
        
        # Load model (cached after first load)
        model = whisper.load_model(settings.whisper_model)
        
        # Transcribe
        result = model.transcribe(file_path)
        
        logger.info("Transcribed audio using local Whisper model")
        return result["text"]
        
    except ImportError:
        logger.warning("Whisper not installed. Install with: pip install openai-whisper")
        return None
    except Exception as e:
        logger.error(f"Local Whisper transcription error: {e}")
        return None


def process_audio_upload(
    file_bytes: bytes,
    file_name: str,
    user_id: str
) -> Tuple[Optional[str], Optional[str]]:
    """
    Process audio upload: save file and transcribe.
    
    Args:
        file_bytes: Audio file content
        file_name: Original filename
        user_id: User ID
        
    Returns:
        Tuple of (file_path, transcript)
    """
    # Upload to Supabase or save locally
    if settings.supabase_url and settings.supabase_anon_key:
        file_path = upload_to_supabase(file_bytes, file_name, user_id)
    else:
        file_path = save_audio_locally(file_bytes, file_name, user_id)
    
    if not file_path:
        return None, None
    
    # Transcribe audio
    transcript = transcribe_audio(file_path)
    
    return file_path, transcript


# ============================================================================
# Audio Format Validation
# ============================================================================

SUPPORTED_FORMATS = [".mp3", ".wav", ".m4a", ".ogg", ".flac"]

def is_supported_audio_format(filename: str) -> bool:
    """
    Check if audio file format is supported.
    
    Args:
        filename: Audio filename
        
    Returns:
        True if format is supported, False otherwise
    """
    ext = os.path.splitext(filename)[1].lower()
    return ext in SUPPORTED_FORMATS
