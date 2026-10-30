"""Fresh synthetic coordinates matching the shared foundation tutorial."""
import torch

def example_inputs() -> torch.Tensor:
    return torch.tensor([[1., 0.], [0., 1.], [1., 1.]], dtype=torch.float64, device="cpu")
