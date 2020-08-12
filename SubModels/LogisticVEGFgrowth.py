import matplotlib.pyplot as plt
import numpy as np

volumes = np.arange(-10, 300, 1)

def LogisticGrowthRate(volume, k=0.07, v0=32):
    maxRate = 5*10**-14
    minRate = 5*10**-15
    rate = minRate
    if volume > 0:
        rate = maxRate / (1 + np.exp(-k * (volume - v0)))
    return rate

rates0 = [LogisticGrowthRate(volume, 0.1, 60) for volume in volumes]
rates1 = [LogisticGrowthRate(volume, 0.07, 32) for volume in volumes]
rates2 = [LogisticGrowthRate(volume, 0.05, 44) for volume in volumes]
rates3 = [LogisticGrowthRate(volume, 0.1, 22) for volume in volumes]
rates4 = [LogisticGrowthRate(volume, 0.2, 10) for volume in volumes]

print(f"rate at volume 0: {rates1[11]}")

fig = plt.figure()
# plt.plot(volumes, rates0, label='k=0.1, v0 = 60')
plt.plot(volumes, rates1, label='k = 0.07, v0 = 32')
# plt.plot(volumes, rates2, label='k=0.05, v0 = 44')
# plt.plot(volumes, rates3, label='k=0.1, v0 = 22')
# plt.plot(volumes, rates4, label='k=0.2, v0 = 10')
plt.xlabel('Volume lost')
plt.ylabel('VEGF growth rate')
plt.title('VEGF Growth Rate Given Volume Lost')
plt.legend()
plt.show()