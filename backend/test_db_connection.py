
import os
import sys
import uuid
import logging
# Add project root to path
sys.path.append(os.getcwd())

from backend.config import settings
from backend.supabase_client import get_supabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    logger.info("Testing Supabase Connection...")
    logger.info(f"URL: {settings.supabase_url}")
    # Don't log full key
    logger.info(f"Key present: {bool(settings.supabase_key)}")
    
    supabase = get_supabase()
    
    # 1. Test User Insert
    user_id = str(uuid.uuid4())
    logger.info(f"Attempting to insert test user: {user_id}")
    
    try:
        user_data = {
            "id": user_id,
            "email": f"test_{user_id[:8]}@example.com",
            "name": "Test User"
        }
        res = supabase.table("users").upsert(user_data).execute()
        logger.info("✅ User table accessible and writable.")
    except Exception as e:
        logger.error(f"❌ Failed to write to 'users': {e}")
        return

    # 2. Test Journal Entry Insert
    logger.info("Attempting to insert test journal entry...")
    try:
        entry_data = {
            "user_id": user_id,
            "text": "This is a test entry.",
            "mood_score": 5,
            "sentiment": 0.5,
            "sentiment_label": "POSITIVE",
            "emotion": "happy",
            "themes": ["test"],
            "suggestions": ["keep testing"]
        }
        res = supabase.table("journal_entries").insert(entry_data).execute()
        logger.info("✅ Journal Entries table accessible and writable.")
        
        # Cleanup
        logger.info("Cleaning up test data...")
        supabase.table("journal_entries").delete().eq("user_id", user_id).execute()
        supabase.table("users").delete().eq("id", user_id).execute()
        
    except Exception as e:
        logger.error(f"❌ Failed to write to 'journal_entries': {e}")

if __name__ == "__main__":
    test_connection()
