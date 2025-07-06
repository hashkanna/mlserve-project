"""Configuration settings for MLServe project."""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    app_name: str = "MLServe API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"
    
    # Model Settings
    model_store_path: Path = Path("models/store")
    default_model: str = "resnet18"
    
    # TorchServe Settings
    torchserve_inference_port: int = 8080
    torchserve_management_port: int = 8081
    torchserve_metrics_port: int = 8082
    
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