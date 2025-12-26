"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "AI/ML Playground API"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 5000))
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/rbm_ai_ml_playground"
    )
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI/ML Model Paths
    MODELS_DIR: str = os.getenv("MODELS_DIR", "./trained_models")
    
    # External APIs
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    # Redis (for caching)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # DevLab Settings
    DEVLAB_DOCKER_IMAGE: str = os.getenv("DEVLAB_DOCKER_IMAGE", "python:3.9-slim")
    DEVLAB_EXECUTION_TIMEOUT: int = int(os.getenv("DEVLAB_EXECUTION_TIMEOUT", "30"))  # seconds
    DEVLAB_MAX_MEMORY_MB: int = int(os.getenv("DEVLAB_MAX_MEMORY_MB", "512"))
    DEVLAB_MAX_CPU_PERCENT: int = int(os.getenv("DEVLAB_MAX_CPU_PERCENT", "50"))
    DEVLAB_NETWORK_ISOLATION: bool = os.getenv("DEVLAB_NETWORK_ISOLATION", "True").lower() == "true"
    
    # Code Execution Security (Medium Level)
    CODE_EXECUTION_SANDBOX: bool = True
    CODE_EXECUTION_SCAN_VIRUS: bool = True
    CODE_EXECUTION_PREVENT_XSS: bool = True
    CODE_EXECUTION_PREVENT_INTRUSION: bool = True
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
