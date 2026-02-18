import torch
from torch import nn


class NeuralNetwork(nn.Module):
    def __init__(self, tau, v_th, output_size, input_size):
        super().__init__()
        self.tau = tau
        self.v_th = v_th
        self.weights = nn.Parameter(torch.rand(output_size, input_size) * 0.5)
        self.v=0

    def reset_state(self, batch_size=1, device='cpu'):
        self.v = torch.zeros(batch_size, self.weights.shape[0], device=device)

    def forward(self, x):
        input_current = torch.matmul(x, self.weights.t())
        self.v = self.v * (1.0 - 1.0/self.tau) + input_current
        spikes = (self.v > self.v_th).float()
        with torch.no_grad():
            self.v[spikes > 0] = 0.0
        return spikes

def fric_made(fric):
    i = 0
    while True:
        g = [0,0,0]
        i += 1
        for j in range(len(fric)):
            if i % fric[j] == 0:
                g[j] = 1.0
            else:
                g[j] = 0.0
        yield g
gen_fric = fric_made([3, 5, 2])
g = []
for i in range(100):
    g.append(next(gen_fric))
snn_layer = NeuralNetwork(input_size=3, output_size=1, tau=10.0, v_th=1.0)
with torch.no_grad():
    snn_layer.weights.copy_(torch.tensor([[0.8, 0.1, 0.7]]))

input_spike = torch.tensor(g)
output_spike = snn_layer(input_spike)
print(output_spike)

