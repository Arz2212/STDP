import math
import random

import numpy as np
from matplotlib import pyplot as plt


class neiron:
    def __init__(self, weth, nam, tau, Vth):
        self.weth = []
        for i in range(nam):
            self.weth.append(weth)
        self.tau = tau
        self.Vth = Vth
        self.v = 0
        self.x = [0] * nam
        self.y = [0] * nam
        self.tau_x = 10
        self.tau_y = 10
        self.F_min = 0.5
        self.F_plus = 0.5
    def step(self, signal):
        signal = np.array(signal)
        in_signal = np.dot(np.array(self.weth), signal)
        self.v = self.v * (1.0 - 1.0 / self.tau) + in_signal
        post_spike = 0
        if self.v > self.Vth:
            post_spike = 1
            self.v = 0
        for i in range(len(self.weth)):
            self.x[i] = self.x[i] * math.exp(-1.0 / self.tau_x) + signal[i]
            self.y[i] = self.y[i] * math.exp(-1.0 / self.tau_y) + post_spike
            if post_spike == 1:
                self.weth[i] += self.F_plus * self.x[i]
            if signal[i] == 1:
                self.weth[i] -= self.F_min * self.y[i]
            self.weth[i] = max(0, min(2, self.weth[i]))
    def get_w(self):
        return self.weth


def rand_make(inpp):
    while True:
        g = []
        # Группа 1 (Половина синапсов): Активные. Вероятность спайка 15%
        for i in range(inpp // 2):
            g.append(1 if random.random() < 0.2 else 0)

        # Группа 2 (Вторая половина): Фоновый шум. Вероятность спайка всего 2%
        for i in range(inpp // 2, inpp):
            g.append(1 if random.random() < 0.02 else 0)
        yield g
gen = rand_make(1000)
nn = neiron(0.5, 1000, 10, 80)
for i in range(10000):
    nn.step(next(gen))
plt.figure(figsize=(10, 6))


plt.hist(nn.get_w(), bins=200, color='royalblue', edgecolor='black', alpha=0.8)

plt.title('Распределение весов синапсов после STDP', fontsize=14)
plt.xlabel('Финальный вес синапса (w)', fontsize=12)
plt.ylabel('Количество синапсов', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()