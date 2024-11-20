import torch.nn as nn


def create_simple_conv_cifar():
    conv_model = nn.Sequential(
        nn.Conv2d(in_channels=3, out_channels=32, kernel_size=5),  # 32x28x28
        nn.BatchNorm2d(32),
        nn.ReLU(),

        # nn.Dropout2d(p=0.2),
        # nn.MaxPool2d(kernel_size=2),

        nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5),  # 64x24x24
        nn.BatchNorm2d(64),
        nn.ReLU(),

        nn.Dropout2d(p=0.2),
        nn.MaxPool2d(kernel_size=2),

        nn.Flatten(),
        nn.Linear(12 * 12 * 64, 256),

        nn.BatchNorm1d(256),
        nn.Dropout(p=0.2),

        nn.ReLU(),
        nn.Linear(256, 10)
    )

    return conv_model
