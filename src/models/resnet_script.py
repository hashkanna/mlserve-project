# image_model/resnet_script.py

import torch.nn as nn
from torchvision import models

class ResNet18(nn.Module):
    def __init__(self):
        super(ResNet18, self).__init__()
        self.model = models.resnet18(pretrained=False)
        self.model.fc = nn.Linear(512, 1000)

    def forward(self, x):
        return self.model(x)
