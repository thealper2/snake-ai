import torch
import torch.nn as nn

class QNet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        # First linear layer: input to hidden
        self.linear1 = nn.Linear(input_size, hidden_size)
        # Second linear layer: hidden to output
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # Apply ReLU activation to the first layer's output
        x = torch.relu(self.linear1(x))
        # Pass through the second linear layer
        x = self.linear2(x)
        # Return the final output
        return x