def count_parameters_conv(in_channels: int, out_channels: int, kernel_size: int, bias: bool):
    return out_channels * (in_channels * kernel_size ** 2 + 1 if bias else 0)
