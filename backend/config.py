"""
Configuration module for Emotion Companion backend.
Loads environment variables and provides application settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Uses pydantic for validation and type safety.
    """
    
    # Supabase Configuration
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_key: str = Field(..., env="SUPABASE_KEY")
    supabase_service_role_key: Optional[str] = Field(None, env="SUPABASE_SERVICE_ROLE_KEY")
    supabase_service_key: Optional[str] = Field(None, env="SUPABASE_SERVICE_KEY")
    
    # Database Configuration
    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/emotion_companion",
        env="DATABASE_URL"
    )
    
    # Application Configuration
    secret_key: str = Field(default="dev-secret-key-change-in-production", env="SECRET_KEY")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # NLP Model Configuration
    use_hf_models: bool = Field(default=True, env="USE_HF_MODELS")
    hf_cache_dir: str = Field(default="./model_cache", env="HF_CACHE_DIR")
    
    # Audio Configuration
    enable_audio: bool = Field(default=False, env="ENABLE_AUDIO")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    whisper_model: str = Field(default="whisper-small", env="WHISPER_MODEL")
    
    # Supabase Storage
    storage_bucket: str = Field(default="audio-files", env="STORAGE_BUCKET")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    cors_origins: str = Field(
        default="http://localhost:8501,http://localhost:3000",
        env="CORS_ORIGINS"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"
    
    def get_cors_origins_list(self) -> list:
        """Parse CORS origins string into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """
    Dependency function to get settings instance.
    Useful for FastAPI dependency injection.
    """
    return settings
