"""
Configuration settings for the application
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/pos_data",
        description="PostgreSQL database URL"
    )
    
    # AI API Keys and Endpoints
    perplexity_api_key: Optional[str] = Field(
        default=None,
        description="Perplexity API key for web research"
    )
    nvidia_llm_url: Optional[str] = Field(
        default=None, 
        description="NVIDIA LLM endpoint URL"
    )
    nvidia_api_key: Optional[str] = Field(
        default=None,
        description="NVIDIA API key"
    )
    
    # Application Settings
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    
    # Agent Configuration
    fuzzy_match_threshold: float = Field(
        default=0.6,
        description="Minimum similarity score for fuzzy matching"
    )
    max_perplexity_tokens: int = Field(
        default=1000,
        description="Maximum tokens for Perplexity API requests"
    )
    agent_log_enabled: bool = Field(
        default=True,
        description="Enable agent action logging"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
