"""Configuration settings for MLServe project."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    app_name: str = "MLServe API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    
    # Model Settings
    default_model: str = "resnet18"
    
    # Ray Serve Settings
    ray_serve_port: int = 8000
    ray_serve_host: str = "0.0.0.0"
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Security
    cors_origins: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()