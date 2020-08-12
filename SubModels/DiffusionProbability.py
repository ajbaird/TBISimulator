# double ModelUtilities::CalculateDiffusionProbability(double x, double deltaX, double timeAfterTBI)
# {
# 	constexpr double D = 0.000104; // Diffusion coefficient of VEGF in [mm^2 / s]
# 	constexpr double sigmaCoefficient = 2. * D * 60;
# 	double sigma = std::sqrt(sigmaCoefficient * timeAfterTBI);
# 	double probability = 1 / sigma / std::sqrt(2 * s_kPi) * std::exp( -(x*x) / 2 / (sigma*sigma)) * deltaX;
# 	return probability;
# }

import numpy as np
import matplotlib.pyplot as plt


time = np.linspace(0, 7*24*60, 1000)
x = np.linspace(0, 100, 100)

def Probability(x, deltaX, time):
    D = 0.000104
    sigmaCoef = 2*D*60
    sigma = np.sqrt(sigmaCoef * time)
    return 1 / sigma / np.sqrt(2*np.pi) * np.exp(-x*x / 2 / sigma / sigma) * deltaX

T, X = np.meshgrid(time, x)
P = Probability(X, 10, T)
P1 = Probability(X, 1, T)

P = np.nan_to_num(P, nan=1)
P1 = np.nan_to_num(P1, nan=1)

P = np.array([[max(min(1, a), 0) for a in b] for b in P])
P1 = np.array([[max(min(1, a), 0) for a in b] for b in P1])

print(((P > 0.6).sum()))
print((P1 > 0.6).sum())

fig = plt.figure()
ax = plt.axes(projection='3d')
s0 = ax.plot_surface(T/60, X, P, label='dx = 10')#, color='blue') #cm.viridis / cm.jet
s0._edgecolors2d = s0._edgecolors3d
s0._facecolors2d = s0._facecolors3d
# s0 = ax.plot_surface(T, X, P1, label='dx = 1', color='orange') #cm.viridis / cm.jet
# s0._edgecolors2d = s0._edgecolors3d
# s0._facecolors2d = s0._facecolors3d

plt.legend()
ax.set_xlabel('Time (hours)')
ax.set_ylabel('distance from \ntbi (mm)')
ax.set_zlabel('probability of \ndiffused vegf here')
ax.set_zlim(0,1)

plt.show()