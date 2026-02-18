import random
import matplotlib.pyplot as plt
class neiron:
    def __init__(self, weth, tau, Vth):
        self.weth = weth
        self.tau = tau
        self.Vth = Vth
        self.v = 0
    def step(self, signal):
        in_signal = sum(w * s for w, s in zip(self.weth, signal))
        self.v = self.v * (1.0 - 1.0 / self.tau) + in_signal
        if self.v > self.Vth:
            self.v = 0
            return 1
        return 0


def rand_make(inpp):
    while True:
        g = []
        for i in range(inpp):
            g.append(random.randint(0, 1))
        yield g

def fric_made(fric):
    i = 0
    while True:
        g = []
        i += 1
        for f in fric:
            if i % f == 0:
                g.append(1)
            else:
                g.append(0)
        yield g
test_neiron = neiron([1], 3, 1.5)
time_steps = 20000
gen_fric = fric_made([3])
input_frequencies = []
output_frequencies = []

for p in range(1, 101):
    mass= []
    gen_fric = fric_made([p])
    spikes_out = 0
    for _ in range(time_steps):
        spikes_out += test_neiron.step(next(gen_fric))

    input_frequencies.append(p**-1)
    output_frequencies.append((spikes_out / time_steps))


plt.figure(figsize=(10, 6))
plt.scatter(input_frequencies, output_frequencies, color='blue', s=20, label='Выходная частота')
plt.grid(visible=True, which='major', color='#666666', linestyle='-', alpha=0.6)
plt.minorticks_on()
plt.grid(visible=True, which='minor', color='#999999', linestyle=':', alpha=0.3)
plt.show()