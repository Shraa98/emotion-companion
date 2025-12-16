"""
Supabase authentication client for Streamlit frontend.
Standalone module that doesn't depend on backend code.
"""

import os
from supabase import create_client, Client

def get_supabase() -> Client:
    """
    Initialize and return Supabase client for authentication.
    
    Uses environment variables:
    - SUPABASE_URL: Your Supabase project URL
    - SUPABASE_KEY: Your Supabase anon/public key
    """
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError(
            "Missing Supabase credentials. "
            "Please set SUPABASE_URL and SUPABASE_KEY environment variables."
        )
    
    return create_client(supabase_url, supabase_key)
