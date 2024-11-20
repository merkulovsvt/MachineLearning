import torch
import torch.nn as nn
import torchvision.transforms as T
from torch import optim
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from tqdm import tqdm


def create_conv_model():
    conv_model = nn.Sequential(
        nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2),

        nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2),

        nn.Flatten(),
        nn.Linear(4 * 4 * 64, 256),
        nn.ReLU(),
        nn.Linear(256, 10)
    )

    return conv_model


def train(model: nn.Module, data_loader: DataLoader, optimizer: Optimizer, loss_fn):
    model.train()

    total = 0
    correct = 0

    mean_loss = 0
    for X, y in data_loader:
        optimizer.zero_grad()

        output = model(X)

        loss = loss_fn(output, y)
        mean_loss += loss.item()

        loss.backward()

        optimizer.step()

        _, y_pred = torch.max(output, 1)
        total += y.size(0)
        correct += (y_pred == y).sum().item()

    print(f'\nTraining loss: {mean_loss / len(data_loader)}')
    print(f'Training accuracy: {round(correct / total * 100, 2)}')


@torch.inference_mode()
def evaluate(model: nn.Module, data_loader: DataLoader, loss_fn):
    model.eval()

    total = 0
    correct = 0

    mean_loss = 0
    for X, y in data_loader:
        output = model(X)

        loss = loss_fn(output, y)
        mean_loss += loss.item()

        _, y_pred = torch.max(output, 1)
        total += y.size(0)
        correct += (y_pred == y).sum().item()

    print(f'\nValidation loss: {mean_loss / len(data_loader)}')
    print(f'Validation accuracy: {round(correct / total * 100, 2)}')

    # if round(correct / total * 100, 2) >= 99.3:
    #     torch.save(model.state_dict(), 'conv_model.pt')
    #     print('Model saved!')


mnist_train = MNIST(
    "Data/mnist",
    train=True,
    download=True,
    transform=T.ToTensor()
)

mnist_valid = MNIST(
    "Data/mnist",
    train=False,
    download=True,
    transform=T.ToTensor()
)

model = create_conv_model()
model.load_state_dict(torch.load('conv_model.pt', weights_only=True))

# train_loader = DataLoader(mnist_train, batch_size=64, shuffle=True)
valid_loader = DataLoader(mnist_valid, batch_size=64, shuffle=False)

optimizer = optim.Adam(model.parameters(), lr=1e-3)
loss_fn = nn.CrossEntropyLoss()

n_epochs = 10

for epoch in tqdm(range(n_epochs), 'Epochs'):
    # train(model, train_loader, optimizer, loss_fn)
    evaluate(model, valid_loader, loss_fn)
