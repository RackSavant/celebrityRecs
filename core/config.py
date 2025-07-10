from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Dict, Any, List, Optional
from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

class APIConfig(BaseSettings):
    """API Keys and Service Configuration"""
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    pinecone_api_key: str = Field(..., env="PINECONE_API_KEY")
    pinecone_environment: str = Field(..., env="PINECONE_ENVIRONMENT")
    elasticsearch_url: str = Field(..., env="ELASTICSEARCH_URL")
    
    @validator('temperature', pre=True)
    def validate_temperature(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Temperature must be between 0 and 1')
        return v

class ModelConfig(BaseSettings):
    """Model Configuration Settings"""
    embedding_dimension: int = Field(512, env="EMBEDDING_DIMENSION")
    default_model: str = Field("gpt-3.5-turbo", env="DEFAULT_MODEL")
    temperature: float = Field(0.7, env="MODEL_TEMPERATURE")
    max_tokens: int = Field(2000, env="MAX_TOKENS")
    
    @validator('embedding_dimension')
    def validate_embedding_dimension(cls, v):
        if v < 128 or v > 2048:
            raise ValueError('Embedding dimension must be between 128 and 2048')
        return v

class AgentConfig(BaseSettings):
    """Agent Configuration Settings"""
    max_iterations: int = Field(5, env="AGENT_MAX_ITERATIONS")
    confidence_threshold: float = Field(0.7, env="CONFIDENCE_THRESHOLD")
    temperature: float = Field(0.7, env="AGENT_TEMPERATURE")
    max_conversation_history: int = Field(10, env="MAX_CONVERSATION_HISTORY")
    
    @validator('max_iterations')
    def validate_max_iterations(cls, v):
        if v < 1 or v > 20:
            raise ValueError('Max iterations must be between 1 and 20')
        return v

class DatabaseConfig(BaseSettings):
    """Database and Vector Store Configuration"""
    vector_store_index: str = Field("fashion-items", env="VECTOR_STORE_INDEX")
    vector_store_dimension: int = Field(512, env="VECTOR_STORE_DIMENSION")
    elasticsearch_index: str = Field("fashion-items", env="ELASTICSEARCH_INDEX")
    
    @validator('vector_store_dimension')
    def validate_vector_store_dimension(cls, v):
        if v < 128 or v > 2048:
            raise ValueError('Vector store dimension must be between 128 and 2048')
        return v

class UIConfig(BaseSettings):
    """UI Configuration Settings"""
    theme: str = Field("light", env="UI_THEME")
    layout: str = Field("wide", env="UI_LAYOUT")
    max_image_size: int = Field(2048, env="MAX_IMAGE_SIZE")
    language: str = Field("en", env="UI_LANGUAGE")
    
    @validator('theme')
    def validate_theme(cls, v):
        if v not in ['light', 'dark', 'system']:
            raise ValueError('Theme must be one of: light, dark, system')
        return v

class Settings(BaseSettings):
    """Main application settings"""
    
    # Basic app settings
    app_name: str = Field("Racksavant", env="APP_NAME")
    app_version: str = Field("1.0.0", env="APP_VERSION")
    debug_mode: bool = Field(False, env="DEBUG_MODE")
    
    # Config groups
    api: APIConfig = APIConfig()
    model: ModelConfig = ModelConfig()
    agent: AgentConfig = AgentConfig()
    database: DatabaseConfig = DatabaseConfig()
    ui: UIConfig = UIConfig()
    
    @validator('debug_mode', pre=True)
    def validate_debug_mode(cls, v):
        return str(v).lower() in ['true', '1', 'yes', 'on']
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        
        # Environment variable naming convention
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )

# Initialize settings
settings = Settings()
