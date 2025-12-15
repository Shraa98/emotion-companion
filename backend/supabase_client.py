import logging
from supabase import create_client, Client
from backend.config import settings

logger = logging.getLogger(__name__)

# Global Supabase client instance
_supabase_client: Client = None

def get_supabase() -> Client:
    """
    Get or create the Supabase client instance.
    """
    global _supabase_client
    
    if _supabase_client is None:
        try:
            url = settings.supabase_url
            # Prefer Service Role Key for backend operations (bypasses RLS)
            key = settings.supabase_service_role_key if hasattr(settings, 'supabase_service_role_key') and settings.supabase_service_role_key else settings.supabase_key
            
            if not url or not key:
                logger.warning("Supabase URL or Key not set. Supabase client will fail if used.")
            
            _supabase_client = create_client(url, key)
            logger.info("Supabase client initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Supabase client: {e}")
            raise
            
    return _supabase_client
