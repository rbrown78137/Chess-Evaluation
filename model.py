import torch
import torch.nn as nn
import time


class EvaluationModel(nn.Module):
    def __init__(self):
        super(EvaluationModel, self).__init__()
        self.input_layers = 12
        self.conv_layer = nn.Sequential(
            nn.Conv2d(self.input_layers, 32, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Upsample(scale_factor=2, mode='nearest'),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.ReLU(inplace=True),
            nn.Flatten(),
        )
        self.ff_body = nn.Sequential(
            nn.Linear(in_features=64 * 16 * 16, out_features=100),
            nn.ReLU(),
            nn.Linear(in_features=100, out_features=20),
            nn.ReLU(),
            nn.Linear(in_features=20, out_features=1),
        )

    def forward(self, input):
        output = self.conv_layer(input)
        output = self.ff_body(output)
        return output