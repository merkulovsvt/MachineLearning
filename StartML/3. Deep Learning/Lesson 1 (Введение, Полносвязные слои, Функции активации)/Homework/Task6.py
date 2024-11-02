import torch


def function02(tensor: torch.Tensor) -> torch.Tensor:
    w = torch.empty(size=[tensor.shape[1]], requires_grad=True, dtype=torch.float32)
    with torch.no_grad():
        w.uniform_(0, 1)
    return w
