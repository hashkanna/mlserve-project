#!/bin/bash

# Build ResNet18 model archive for TorchServe

torch-model-archiver \
  --model-name resnet18 \
  --version 1.0 \
  --model-file src/models/resnet_script.py \
  --serialized-file models/resnet18.pt \
  --handler image_classifier \
  --export-path models/store \
  --force

echo "Model archive created at models/store/resnet18.mar"

