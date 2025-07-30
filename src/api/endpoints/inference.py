"""Inference endpoints."""

from typing import List, Dict, Any, Optional
import logging

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import ray
from ray import serve

from src.services.ray_serve import ModelRequest, ModelResponse

router = APIRouter()
logger = logging.getLogger(__name__)

# Global registry handle
_registry_handle: Optional[serve.handle] = None


class InferenceRequest(BaseModel):
    """Model inference request."""
    model: str
    data: List[List[float]]  # Assuming image data as nested lists
    
    
class InferenceResponse(BaseModel):
    """Model inference response."""
    model: str
    predictions: List[Dict[str, Any]]


async def get_registry_handle():
    """Get Ray Serve registry handle."""
    global _registry_handle
    if _registry_handle is None:
        try:
            # Get the deployment handle from the "registry" app
            _registry_handle = serve.get_app_handle("registry")
        except Exception as e:
            logger.error(f"Failed to get registry handle: {e}")
            raise HTTPException(
                status_code=503,
                detail="Model service not available"
            )
    return _registry_handle


@router.post("/predict", response_model=InferenceResponse)
async def predict(
    request: InferenceRequest,
    registry=Depends(get_registry_handle)
):
    """Run model inference using Ray Serve."""
    try:
        # Create model request
        model_request = ModelRequest(data=request.data)
        
        # Get prediction from Ray Serve
        model_response = await registry.predict.remote(request.model, model_request)
        
        return InferenceResponse(
            model=request.model,
            predictions=model_response.predictions
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during prediction"
        )


@router.get("/models")
async def list_models(registry=Depends(get_registry_handle)):
    """List available models from Ray Serve registry."""
    try:
        models = await registry.list_models.remote()
        return {"models": models}
    except Exception as e:
        logger.error(f"Failed to list models: {e}")
        raise HTTPException(
            status_code=503,
            detail="Model service not available"
        )


@router.get("/ray/status")
async def ray_status():
    """Get Ray cluster status."""
    try:
        if not ray.is_initialized():
            return {"status": "not_initialized", "ray_initialized": False}
        
        # Get Ray cluster resources
        resources = ray.cluster_resources()
        available = ray.available_resources()
        
        # Get Ray Serve status
        serve_status = "not_started"
        deployments = []
        
        try:
            deployment_info = serve.list_deployments()
            serve_status = "running"
            deployments = [
                {
                    "name": name,
                    "status": info.status,
                    "num_replicas": info.deployment_config.num_replicas,
                }
                for name, info in deployment_info.items()
            ]
        except Exception:
            pass
        
        return {
            "status": "running",
            "ray_initialized": True,
            "resources": {
                "total": dict(resources),
                "available": dict(available),
            },
            "serve": {
                "status": serve_status,
                "deployments": deployments,
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get Ray status: {e}")
        return {
            "status": "error",
            "error": str(e)
        }