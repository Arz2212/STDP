import math
import random
import matplotlib.pyplot as plt
class neiron:
    def __init__(self, weth, tau, Vth):
        self.weth = weth
        self.tau = tau
        self.Vth = Vth
        self.v = 0
        self.x = 0
        self.y = 0
        self.tau_x = 10
        self.tau_y = 10
        self.F_min = 0.05
        self.F_plus = 0.0525
    def step(self, signal):
        in_signal = self.weth* signal
        self.v = self.v * (1.0 - 1.0 / self.tau) + in_signal
        self.x = self.x * math.exp(-1.0 / self.tau_x) + signal
        post_spike = 0
        if self.v > self.Vth:
            post_spike = 1
            self.v = 0
        self.y = self.y * math.exp(-1.0 / self.tau_y) + post_spike
        if post_spike == 1:
            self.weth += self.F_plus * self.x
        if signal == 1:
            self.weth -= self.F_min * self.y
        self.weth = max(0, min(2, self.weth))
    def get_w(self):
        return self.weth


def rand_make(inpp):
    while True:
        g = []
        for i in range(inpp):
            g.append(1 if random.random() < 0.2 else 0 )
        yield g[0]
f = []
for i in range(1000):
    test_neiron = neiron(1, 10, 4.5)
    gen_rand = rand_make(1)
    for _ in range(10000):
        test_neiron.step(next(gen_rand))
    f.append(test_neiron.get_w())
print(f)
plt.figure(figsize=(10, 6))

# Рисуем гистограмму. bins=20 означает, что мы разобьем ось X на 20 столбиков
plt.hist(f, bins=200, color='royalblue', edgecolor='black', alpha=0.8)

plt.title('Распределение весов одиночных синапсов после STDP', fontsize=14)
plt.xlabel('Финальный вес синапса (w)', fontsize=12)
plt.ylabel('Количество экспериментов', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()