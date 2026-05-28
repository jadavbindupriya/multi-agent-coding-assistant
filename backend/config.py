# backend/config.py
"""
Configuration settings for the backend.
Centralized place for all settings and environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Settings class that loads all configuration.
    
    Why a class?
    - Centralized: All settings in one place
    - Professional: Real projects do this
    - Easy to extend: Add new settings later
    """
    
    # ==================== API Keys ====================
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    CLAUDE_API_KEY: str = os.getenv("CLAUDE_API_KEY", "")
    
    # ==================== FastAPI Configuration ====================
    API_TITLE: str = "Multi-Agent Coding Assistant"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "An AI system with multiple agents working together to solve coding tasks"
    
    # ==================== Server Configuration ====================
    DEBUG: bool = True  # Set to False in production
    ENVIRONMENT: str = "development"  # or "production"
    
    # ==================== Model Configuration ====================
    DEFAULT_MODEL: str = "gpt-4"  # Which model to use
    DEFAULT_TEMPERATURE: float = 0.7  # Balance between creativity and consistency
    DEFAULT_MAX_TOKENS: int = 1000  # Default max output length
    
    # ==================== Logging Configuration ====================
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # ==================== Validation ====================
    MAX_TASK_LENGTH: int = 5000  # Max characters per task input
    MAX_RESPONSE_TIME: int = 60  # Max seconds to wait for response

# Create a global settings instance
settings = Settings()

# Verify API keys are loaded
if not settings.OPENAI_API_KEY and not settings.CLAUDE_API_KEY:
    print("⚠️  WARNING: No API keys found in .env file!")
    print("   Set OPENAI_API_KEY or CLAUDE_API_KEY in your .env file")