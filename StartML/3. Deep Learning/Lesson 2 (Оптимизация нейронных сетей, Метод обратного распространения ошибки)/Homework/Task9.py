from collections import OrderedDict

import torch
import torch.nn as nn
from torch import optim
from torch.optim import Optimizer
from torch.utils.data import DataLoader, TensorDataset


def create_model():
    model = nn.Sequential(
        OrderedDict(
            [
                ('linear1', nn.Linear(in_features=100, out_features=10)),
                ('relu', nn.ReLU()),
                ('linear2', nn.Linear(in_features=10, out_features=1))
            ]
        )
    )

    return model


def train(model: nn.Module, data_loader: DataLoader, optimizer: Optimizer, loss_fn):
    model.train()

    mean_loss = 0
    for X, y in loader:
        optimizer.zero_grad()

        output = model(X)

        loss = loss_fn(output, y)
        loss.backward()

        mean_loss += loss.item()

        optimizer.step()

    return mean_loss / len(data_loader), model.parameters()


n_features = 100
n_objects = 100

w_true = torch.randn(n_features)

X = (torch.rand(n_objects, n_features) - 0.5) * 10
X *= (torch.arange(n_features) * 2 + 1)
Y = (X @ w_true + torch.randn(n_objects)).unsqueeze(1)

model = create_model()
dataset = TensorDataset(X, Y)
loader = DataLoader(dataset, batch_size=20, shuffle=True)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.MSELoss()

loss, parameters = train(model, loader, optimizer, loss_fn)
print(f'final - {loss}')
