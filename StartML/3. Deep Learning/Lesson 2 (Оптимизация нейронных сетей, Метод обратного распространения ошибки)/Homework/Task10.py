import torch
from torch import nn
from torch.utils.data import DataLoader


@torch.inference_mode()
def evaluate(model: nn.Module, data_loader: DataLoader, loss_fn):
    model.eval()

    mean_loss = 0
    for X, y in data_loader:
        output = model(X)

        loss = loss_fn(output, y)
        mean_loss += loss.item()

    return mean_loss / len(data_loader)
