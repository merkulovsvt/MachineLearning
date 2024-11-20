from collections import OrderedDict

import torch
import torch.nn as nn
import torchvision.transforms as T
from torch import optim
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST


@torch.inference_mode()
def predict(model: nn.Module, loader: DataLoader, device: torch.device):
    model.eval()
    res = torch.Tensor(device=device)

    for x, y in loader:
        output = model(x)
        _, y_ped = torch.max(output, 1)
        res = torch.cat([res, y_ped], 0)
    return res


mnist_valid = MNIST(
    "Data/mnist",
    train=False,
    download=True,
    transform=T.ToTensor()
)

model = nn.Sequential(OrderedDict([
    ('f', nn.Flatten()),
    ('l1', nn.Linear(28 * 28, 512)),
    ('relu1', nn.ReLU()),
    ('l2', nn.Linear(512, 256)),
    ('relu2', nn.ReLU()),
    ('l3', nn.Linear(256, 10))
]))

valid_loader = DataLoader(mnist_valid, batch_size=64, shuffle=False)
optimizer = optim.Adam(model.parameters(), lr=2e-3)

predict(model, valid_loader, torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))
