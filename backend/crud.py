"""
CRUD (Create, Read, Update, Delete) operations for database entities.
Refactored to use Supabase Python Client (REST API) instead of direct PostgreSQL connection.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
import json
import logging
from datetime import datetime

from backend.supabase_client import get_supabase
from backend.models import JournalEntryCreate, UserCreate

logger = logging.getLogger(__name__)


# ============================================================================
# User CRUD Operations
# ============================================================================

def create_user(user_data: UserCreate) -> Optional[Dict[str, Any]]:
    """
    Create a new user in the database.
    """
    supabase = get_supabase()
    
    data = {
        "email": user_data.email,
        "name": user_data.name
    }
    
    try:
        # Supabase performs an upsert by default if we don't specify otherwise? 
        # Actually .insert() fails on conflict usually.
        # But we can try to select first or just insert and handle error.
        response = supabase.table("users").insert(data).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        logger.exception("Database operation failed")
        raise


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get user by email address."""
    supabase = get_supabase()
    try:
        response = supabase.table("users").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        return None


def get_user_by_id(user_id: UUID) -> Optional[Dict[str, Any]]:
    """Get user by ID."""
    supabase = get_supabase()
    try:
        response = supabase.table("users").select("*").eq("id", str(user_id)).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"Error getting user by id: {e}")
        return None


# ============================================================================
# Journal Entry CRUD Operations
# ============================================================================

def create_journal_entry(
    user_id: UUID,
    text: str,
    analysis: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """
    Create a new journal entry with analysis results.
    """
    supabase = get_supabase()
    
    # Extract analysis components
    sentiment = analysis.get("sentiment", {})
    emotion = analysis.get("emotion", {})
    
    # Prepare data object matching Supabase columns
    # Note: JSON fields are passed as dictionaries directly to supabase-py, 
    # it handles serialization usually, or we pass dicts.
    
    data = {
        "user_id": str(user_id),
        "text": text,
        "mood_score": analysis.get("mood_score"),
        "sentiment": sentiment.get("score"),
        "sentiment_label": sentiment.get("label"),
        "emotion": emotion.get("primary_emotion"),
        "emotion_scores": emotion.get("emotion_scores", {}),
        "themes": analysis.get("themes", []),
        "highlighted_phrases": analysis.get("highlighted_phrases", {}),
        "suggestions": analysis.get("suggestions", []),
        "metadata": analysis.get("metadata", {})
    }
    
    # Ensure user exists to satisfy Foreign Key constraint
    try:
        # User UPSERT pattern
        supabase.table("users").upsert({
            "id": str(user_id),
            "email": f"user_{str(user_id)[:8]}@example.com",
            "name": "Anonymous User"
        }, on_conflict="id").execute()
    except Exception:
        # Pass silently - if upsert fails, the main insert will fail with FK constraint too,
        # but this is much safer than blind inserts.
        pass

    try:
        response = supabase.table("journal_entries").insert(data).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        logger.exception("Database operation failed")
        raise


def get_journal_entries(
    user_id: UUID,
    limit: int = 50,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """
    Get journal entries for a user with pagination.
    """
    supabase = get_supabase()
    try:
        # range is 0-based inclusive start, exclusive end? No, Supabase range is inclusive-inclusive usually [from, to]
        # offset=0, limit=50 -> range(0, 49)
        start = offset
        end = offset + limit - 1
        
        response = supabase.table("journal_entries") \
            .select("*") \
            .eq("user_id", str(user_id)) \
            .order("created_at", desc=True) \
            .range(start, end) \
            .execute()
            
        return response.data
    except Exception as e:
        logger.error(f"Error fetching journal entries: {e}")
        return []


def get_journal_entry(entry_id: UUID) -> Optional[Dict[str, Any]]:
    """Get a single journal entry by ID."""
    supabase = get_supabase()
    try:
        response = supabase.table("journal_entries").select("*").eq("id", str(entry_id)).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        logger.error(f"Error fetching journal entry: {e}")
        return None


def count_user_entries(user_id: UUID) -> int:
    """Count total journal entries for a user."""
    supabase = get_supabase()
    try:
        # count='exact' param needed
        response = supabase.table("journal_entries") \
            .select("id", count="exact") \
            .eq("user_id", str(user_id)) \
            .execute()
        return response.count
    except Exception as e:
        logger.error(f"Error counting user entries: {e}")
        return 0


# ============================================================================
# Audio Entry CRUD Operations
# ============================================================================

def create_audio_entry(
    user_id: UUID,
    file_path: str,
    file_name: str,
    file_size: int,
    transcript: Optional[str] = None,
    analysis: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Create a new audio entry record.
    """
    supabase = get_supabase()
    
    # Extract analysis if provided
    sentiment = analysis.get("sentiment", {}) if analysis else {}
    emotion = analysis.get("emotion", {}) if analysis else {}
    status = "completed" if transcript else "pending"
    
    data = {
        "user_id": str(user_id),
        "file_path": file_path,
        "file_name": file_name,
        "file_size": file_size,
        "transcript": transcript,
        "transcription_status": status,
        "mood_score": analysis.get("mood_score") if analysis else None,
        "sentiment": sentiment.get("score"),
        "sentiment_label": sentiment.get("label"),
        "emotion": emotion.get("primary_emotion"),
        "emotion_scores": emotion.get("emotion_scores", {}) if emotion else None,
        "themes": analysis.get("themes", []) if analysis else [],
        "suggestions": analysis.get("suggestions", []) if analysis else [],
        "metadata": analysis.get("metadata", {}) if analysis else {}
    }
    
    # Ensure user exists to satisfy Foreign Key constraint
    try:
        supabase.table("users").upsert({
            "id": str(user_id),
            "email": f"user_{str(user_id)[:8]}@example.com",
            "name": "Anonymous User"
        }, on_conflict="id").execute()
    except Exception:
        pass

    try:
        response = supabase.table("audio_entries").insert(data).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        logger.exception("Database operation failed")
        raise


def get_audio_entries(user_id: UUID, limit: int = 50) -> List[Dict[str, Any]]:
    """Get audio entries for a user."""
    supabase = get_supabase()
    try:
        response = supabase.table("audio_entries") \
            .select("*") \
            .eq("user_id", str(user_id)) \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        return response.data
    except Exception as e:
        logger.error(f"Error fetching audio entries: {e}")
        return []
