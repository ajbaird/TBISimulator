# Plot VEGF ODEs
# Transferred from Jupyter Notebook

# https://apmonitor.com/pdc/index.php/Main/SolveDifferentialEquations

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def mySystemODEs(y, t):
    L = y[0]  # VEGF Ligand
    R = y[1]  # VEGFR Receptor
    LR = y[2]  # VEGF-VEGFR Ligand-Receptor complex

    def LogisticGrowthRateR(vegf, k=6 * 10 ** 10, v0=3 * 10 ** -11):
        maxRate = 7.5 * 10 ** -13
        minRate = 2.4 * 10 ** -13
        rate = minRate
        if vegf > 1.2 * 10 ** -11:
            rate = maxRate / (1 + np.exp(-k * (vegf - v0))) + 1.75 * 10 ** -13
        return rate

    volume = 0
    v0 = 60
    k = 0.1
    aL = 10 ** -12 / (1 + np.exp(-k * (volume - v0)))



    # New New Model:
    aL = 2 * 10 ** -14  # 10**-13/-12 growth rate VEGF
    rL = .8 * 10 ** -4  # removal rate coefficient VEGF
    ka = 1 * 10 ** 6  # association rate coefficient
    kd = 15 * 10 ** -4  # dissociation rate coefficient
    aR = LogisticGrowthRateR(L, 13 * 10 ** 10, 3 * 10 ** -11) # 2 * L / 100  # 10**-13/-12 growth rate VEGFR
    rR = rL  # removal rate coefficient VEGFR
    iLR = .5 * 10 ** -4  # internalization (removal) rate coefficient VEGF-VEGFR

    # New Model:
    # aL = 5 * 10 ** -14  # 10**-13/-12 growth rate VEGF
    # rL = 3 * 10 ** -4  # removal rate coefficient VEGF
    # ka = 1 * 10 ** 6  # association rate coefficient
    # kd = 1 * 10 ** -4  # dissociation rate coefficient
    # aR = aL * 7  # 10**-13/-12 growth rate VEGFR
    # rR = rL  # removal rate coefficient VEGFR
    # iLR = 3 * 10 ** -4  # internalization (removal) rate coefficient VEGF-VEGFR

    dLdt = aL - rL * L - ka * L * R + kd * LR
    dRdt = aR - rR * R - ka * L * R + kd * LR
    dLRdt = ka * L * R - kd * LR - iLR * LR

    # x 60 to convert M/s to M/min
    return [60 * dLdt, 60 * dRdt, 60 * dLRdt]

t = np.linspace(0, 3*1440)
#t = np.linspace(4*2880, 10*2880)
# y0 = [13*10**-12, .11*10**-9, 3.7*10**-12]
y0 = [12*10**-12, 3*10**-9, 20*10**-12]
y = odeint(mySystemODEs, y0, t)
fig = plt.figure()
plt.title('Normalized and Absolute Concentrations\nwhen high growth conditions are applied to steady state')
ax1 = fig.add_subplot(1, 2, 1)
ax1.plot(t/60/24, y[:,0]/y0[0], label="[L]")
ax1.plot(t/60/24, y[:,1]/y0[1], label='[R]')
ax1.plot(t/60/24, y[:,2]/y0[2], label='[LR]')
ax1.set_xlabel('time(days)')
ax1.set_ylabel('Normalized concentration')

ax2 = fig.add_subplot(1, 2, 2)
ax2.plot(t/60/24, y[:,0], label="[L]")
ax2.plot(t/60/24, y[:,1], label='[R]')
ax2.plot(t/60/24, y[:,2], label='[LR]')
ax2.set_xlabel('time(days)')
ax2.set_ylabel('Absolute concentration')
ax2.yaxis.set_label_position('right')
ax2.yaxis.tick_right()

plt.legend()
plt.show()