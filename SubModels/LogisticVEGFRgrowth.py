import matplotlib.pyplot as plt
import numpy as np

vegfs = np.linspace(1*10**-11, 6*10**-11, 1000)

def LogisticGrowthRateR(vegf, k=6*10**10, v0=3*10**-11):
    maxRate = 7.5*10**-13
    minRate = 2.4*10**-13
    rate = minRate
    if vegf > 1.2*10**-11:
        rate = maxRate / (1 + np.exp(-k * (vegf - v0))) + 1.75*10**-13
    return rate

k0 = 13*10**10
v0 = 3*10**-11
rates0 = [LogisticGrowthRateR(vegf, k0, v0) for vegf in vegfs]
k1 = 69314718056
v1 = 3*10**-11
rates1 = [LogisticGrowthRateR(vegf, k1, v1) for vegf in vegfs]
k2 = 12*10**10
v2 = 3*10**-11
rates2 = [LogisticGrowthRateR(vegf, k2, v2) for vegf in vegfs]

fig = plt.figure()
plt.plot(vegfs, rates0, label=f'k={k0}, v0={v0}')
# plt.plot(vegfs, rates1, label=f'k={k1}, v0={v1}')
# plt.plot(vegfs, rates2, label=f'k={k2}, v0={v2}')

plt.xlabel('[vegf]')
plt.ylabel('VEGFR growth rate')
plt.legend()
plt.title("Model VEGFR Growth Rate vs [VEGF]")
plt.show()