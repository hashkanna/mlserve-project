"""Ray Serve configuration."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class AutoscalingConfig(BaseModel):
    """Autoscaling configuration for Ray Serve deployments."""
    min_replicas: int = Field(default=1, ge=1)
    max_replicas: int = Field(default=3, ge=1)
    target_num_ongoing_requests_per_replica: int = Field(default=10, ge=1)
    upscale_delay_s: float = Field(default=3.0, ge=0)
    downscale_delay_s: float = Field(default=30.0, ge=0)


class DeploymentConfig(BaseModel):
    """Configuration for a Ray Serve deployment."""
    name: str
    num_replicas: Optional[int] = Field(default=None, ge=1)
    ray_actor_options: Dict[str, Any] = Field(
        default_factory=lambda: {"num_cpus": 1, "num_gpus": 0}
    )
    autoscaling_config: Optional[AutoscalingConfig] = Field(default_factory=AutoscalingConfig)
    health_check_period_s: float = Field(default=10.0, ge=1)
    health_check_timeout_s: float = Field(default=30.0, ge=1)
    graceful_shutdown_timeout_s: float = Field(default=20.0, ge=0)
    graceful_shutdown_wait_loop_s: float = Field(default=2.0, ge=0)


class RayServeConfig(BaseModel):
    """Ray Serve configuration."""
    http_options: Dict[str, Any] = Field(
        default_factory=lambda: {
            "host": "0.0.0.0",
            "port": 8001,
            "root_path": "/ray",
            "middlewares": [],
        }
    )
    grpc_options: Dict[str, Any] = Field(
        default_factory=lambda: {
            "port": 9001,
            "grpc_servicer_functions": [],
        }
    )
    logging_config: Dict[str, Any] = Field(
        default_factory=lambda: {
            "log_level": "INFO",
            "logs_dir": None,
            "enable_access_log": True,
        }
    )


# Default configurations for different model types
MODEL_CONFIGS = {
    "resnet18": DeploymentConfig(
        name="resnet18",
        ray_actor_options={"num_cpus": 2, "num_gpus": 0},
        autoscaling_config=AutoscalingConfig(
            min_replicas=1,
            max_replicas=5,
            target_num_ongoing_requests_per_replica=5,
        ),
    ),
    "resnet50": DeploymentConfig(
        name="resnet50",
        ray_actor_options={"num_cpus": 4, "num_gpus": 0.5},
        autoscaling_config=AutoscalingConfig(
            min_replicas=1,
            max_replicas=3,
            target_num_ongoing_requests_per_replica=3,
        ),
    ),
    "vit": DeploymentConfig(
        name="vit",
        ray_actor_options={"num_cpus": 4, "num_gpus": 1},
        autoscaling_config=AutoscalingConfig(
            min_replicas=1,
            max_replicas=2,
            target_num_ongoing_requests_per_replica=2,
        ),
    ),
}


def get_deployment_config(model_name: str) -> DeploymentConfig:
    """Get deployment configuration for a model."""
    return MODEL_CONFIGS.get(
        model_name,
        DeploymentConfig(
            name=model_name,
            ray_actor_options={"num_cpus": 1, "num_gpus": 0},
        ),
    )


# Ray cluster configuration
RAY_INIT_CONFIG = {
    "dashboard_host": "0.0.0.0",
    "dashboard_port": 8265,
    "include_dashboard": True,
    "num_cpus": None,  # Use all available CPUs
    "num_gpus": None,  # Use all available GPUs
    "log_to_driver": True,
    "logging_level": "INFO",
}