import torch


def function04(x: torch.Tensor, y: torch.Tensor):
    layer = torch.nn.Linear(in_features=x.shape[1], out_features=1, bias=True)

    mse = float("+inf")
    step_size = 1e-2
    while mse >= 0.3:
        mse = torch.mean((layer(x).ravel() - y) ** 2)

        mse.backward()

        with torch.no_grad():
            layer.weight -= layer.weight.grad * step_size
            layer.bias -= layer.bias.grad * step_size

        layer.zero_grad()

    return layer

