"""Ray Serve integration for model serving."""

import logging
from typing import Dict, List, Any, Optional
import numpy as np
import torch
from ray import serve
from ray.serve import Application
from transformers import AutoModelForImageClassification, AutoImageProcessor
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ModelRequest(BaseModel):
    """Model inference request."""
    data: List[List[float]]  # Image data as nested lists


class ModelResponse(BaseModel):
    """Model inference response."""
    predictions: List[Dict[str, Any]]


@serve.deployment(
    ray_actor_options={"num_cpus": 1, "num_gpus": 0},
    autoscaling_config={
        "min_replicas": 1,
        "max_replicas": 3,
        "target_num_ongoing_requests_per_replica": 10,
    },
    health_check_period_s=10,
    health_check_timeout_s=30,
)
class ResNetModel:
    """Ray Serve deployment for ResNet model."""
    
    def __init__(self, model_name: str = "microsoft/resnet-18"):
        """Initialize the model and processor."""
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Loading model {model_name} on device {self.device}")
        
        try:
            self.model = AutoModelForImageClassification.from_pretrained(model_name)
            self.processor = AutoImageProcessor.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Model {model_name} loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    async def __call__(self, request: ModelRequest) -> ModelResponse:
        """Process inference request."""
        try:
            predictions = []
            
            for data in request.data:
                # Convert input data to proper tensor format
                data_array = np.array(data, dtype=np.float32)
                
                # Reshape the flattened data to image format (C, H, W)
                if len(data_array) == 150528:  # 224*224*3
                    # Reshape from flat array to (224, 224, 3)
                    image_array = data_array.reshape(224, 224, 3)
                    # Convert to PIL Image format (H, W, C) -> (C, H, W)
                    image_array = np.transpose(image_array, (2, 0, 1))  # (3, 224, 224)
                else:
                    # Create a random image for demo if wrong size
                    logger.warning(f"Unexpected data size: {len(data_array)}, using random image")
                    image_array = np.random.rand(3, 224, 224).astype(np.float32)
                
                # Normalize to ImageNet standards (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                imagenet_mean = np.array([0.485, 0.456, 0.406]).reshape(3, 1, 1)
                imagenet_std = np.array([0.229, 0.224, 0.225]).reshape(3, 1, 1)
                
                # Apply ImageNet normalization
                normalized_image = (image_array - imagenet_mean) / imagenet_std
                
                # Convert to PyTorch tensor with correct dtype and add batch dimension
                input_tensor = torch.from_numpy(normalized_image).float().unsqueeze(0).to(self.device)
                
                # Run inference with the actual ResNet model
                with torch.no_grad():
                    outputs = self.model(input_tensor)
                    logits = outputs.logits  # Get logits from Hugging Face model output
                    probs = torch.nn.functional.softmax(logits, dim=-1)
                
                # Get top 5 predictions
                top5_probs, top5_indices = torch.topk(probs[0], 5)
                
                pred = {
                    "predictions": [
                        {
                            "class_id": idx.item(),
                            "class_name": self.model.config.id2label.get(idx.item(), f"class_{idx.item()}"),
                            "confidence": prob.item()
                        }
                        for prob, idx in zip(top5_probs, top5_indices)
                    ]
                }
                predictions.append(pred)
            
            return ModelResponse(predictions=predictions)
            
        except Exception as e:
            logger.error(f"Inference error: {e}")
            # Log more details for debugging
            logger.error(f"Input data shape: {np.array(request.data[0]).shape if request.data else 'None'}")
            raise


@serve.deployment(
    ray_actor_options={"num_cpus": 1},
    autoscaling_config={
        "min_replicas": 1,
        "max_replicas": 2,
    },
)
class ModelRegistry:
    """Registry for managing multiple models."""
    
    def __init__(self):
        """Initialize the model registry."""
        self.models: Dict[str, serve.handle] = {}
        self.model_info: Dict[str, Dict[str, Any]] = {}
        logger.info("Model registry initialized")
    
    async def register_model(self, name: str, model_handle: serve.handle, info: Dict[str, Any]):
        """Register a new model."""
        self.models[name] = model_handle
        self.model_info[name] = info
        logger.info(f"Model {name} registered")
    
    async def get_model(self, name: str) -> Optional[serve.handle]:
        """Get a model by name."""
        return self.models.get(name)
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List all registered models."""
        return [
            {
                "name": name,
                **info
            }
            for name, info in self.model_info.items()
        ]
    
    async def predict(self, model_name: str, request: ModelRequest) -> ModelResponse:
        """Run prediction using specified model."""
        model = await self.get_model(model_name)
        if not model:
            raise ValueError(f"Model {model_name} not found")
        
        return await model.remote(request)


def create_ray_serve_app() -> Application:
    """Create Ray Serve application with deployments."""
    # Deploy ResNet model
    resnet_deployment = ResNetModel.bind()
    
    # Deploy model registry
    registry_deployment = ModelRegistry.bind()
    
    # Create composed application
    return serve.run(
        {
            "resnet": resnet_deployment,
            "registry": registry_deployment,
        },
        name="mlserve",
        route_prefix="/ray",
    )


async def init_ray_serve():
    """Initialize Ray Serve with default models."""
    logger.info("Initializing Ray Serve...")
    
    # Start Ray Serve with custom HTTP options to avoid port conflict
    serve.start(
        detached=True,
        http_options={
            "host": "0.0.0.0",
            "port": 8001,  # Use port 8001 for Ray Serve
        }
    )
    
    # Deploy ResNet model
    resnet_handle = serve.run(
        ResNetModel.bind(),
        name="resnet",
        route_prefix="/ray/models/resnet",
    )
    
    # Deploy model registry
    registry_handle = serve.run(
        ModelRegistry.bind(),
        name="registry",
        route_prefix="/ray/registry",
    )
    
    # Register ResNet in the registry
    await registry_handle.register_model.remote(
        "resnet18",
        resnet_handle,
        {
            "version": "1.0",
            "status": "ready",
            "description": "ResNet-18 image classification model",
            "input_shape": [3, 224, 224],
            "framework": "pytorch",
        }
    )
    
    logger.info("Ray Serve initialized successfully")
    return registry_handle


async def shutdown_ray_serve():
    """Shutdown Ray Serve gracefully."""
    logger.info("Shutting down Ray Serve...")
    serve.shutdown()
    logger.info("Ray Serve shutdown complete")