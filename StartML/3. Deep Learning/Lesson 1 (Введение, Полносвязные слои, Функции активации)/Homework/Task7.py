import torch


def function02(tensor: torch.Tensor) -> torch.Tensor:
    w = torch.empty(size=[tensor.shape[1]], requires_grad=True, dtype=torch.float32)
    with torch.no_grad():
        w.uniform_(0, 1)
    return w


def function03(X: torch.Tensor, Y: torch.Tensor) -> torch.Tensor:
    w = function02(tensor=X)

    mse = float("+inf")
    step_size = 1e-2

    while mse >= 1:
        mse = torch.mean((X @ w - Y) ** 2)
        mse.backward()

        with torch.no_grad():
            w -= w.grad * step_size

        w.grad.zero_()
    return w
