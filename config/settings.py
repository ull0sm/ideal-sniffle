"""Configuration settings for the Boeing India Chatbot."""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # App Info
    APP_NAME: str = "Boeing India Career Chatbot"
    APP_VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URI: str = os.getenv("DATABASE_URI", "")
    
    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    LANGSEARCH_API_KEY: str = os.getenv("LANGSEARCH_API_KEY", "")
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    OAUTH_REDIRECT_URI: str = os.getenv("OAUTH_REDIRECT_URI", "http://localhost:8501")
    
    # Admin
    ADMIN_EMAILS: List[str] = []
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    RATE_LIMIT_PER_HOUR: int = 100
    
    # LLM Settings
    MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.7
    
    # Conversation Settings
    MAX_HISTORY_MESSAGES: int = 20
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse admin emails from environment
        admin_emails_str = os.getenv("ADMIN_EMAILS", "")
        if admin_emails_str:
            self.ADMIN_EMAILS = [email.strip() for email in admin_emails_str.split(",")]


settings = Settings()
