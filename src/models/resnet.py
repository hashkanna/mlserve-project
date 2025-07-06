#!/usr/bin/env python3
"""Script to download and save ResNet18 model weights."""

import torch
import torchvision.models as models
from pathlib import Path


def download_resnet18():
    """Download pre-trained ResNet18 model and save weights."""
    # Create models directory if it doesn't exist
    models_dir = Path(__file__).parent.parent.parent / "models"
    models_dir.mkdir(exist_ok=True)
    
    # Download model with new weights parameter
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    
    # Save model state dict
    output_path = models_dir / "resnet18.pt"
    torch.save(model.state_dict(), output_path)
    print(f"Model saved to {output_path}")


if __name__ == "__main__":
    download_resnet18()
