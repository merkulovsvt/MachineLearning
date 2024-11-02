import torch.nn as nn


def create_model():
    model = nn.Sequential(nn.Linear(in_features=100, out_features=10),
                          nn.ReLU(),
                          nn.Linear(in_features=10, out_features=1))
    return model
