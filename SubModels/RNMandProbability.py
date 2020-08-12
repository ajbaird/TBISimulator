# if ... && randomNumber * m_randNumMultiplier < probability * boundLink && ...
# then new sprout will form
# Above method favors small randomNumber's for new sprouts

# Alt method below to favor larger randomNumber's
# randomNumber * boundLink * m_randNumMultiplier > 1 - probability
# 1 - randomNumber * boundLink * m_randNumMultiplier < probability

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.ticker as ticker

rans = np.arange(0, 1, 0.01)
vegf = np.arange(1, 19, 1)

def CalcValue(ranNum, vegf, link):
    return 150*ranNum/(vegf**link)

def AltCalcMinProb(ranNum, vegf, link):
    return 1 - ranNum * vegf**link / 10**link

def AltCalcMinProb2(ranNum, vegf, link):
    return 1 - ranNum * vegf**link / 10

R, V = np.meshgrid(rans, vegf)

Z0 = CalcValue(R, V, 0)
Z1 = CalcValue(R, V, 1)
Z2 = CalcValue(R, V, 2)
Z3 = CalcValue(R, V, 3)

fig = plt.figure()
ax = plt.axes(projection='3d')
# s0 = ax.plot_surface(R, V, Z0, label='link 0', color='yellow') #cm.viridis / cm.jet
# s0._edgecolors2d = s0._edgecolors3d
# s0._facecolors2d = s0._facecolors3d
s1 = ax.plot_surface(R, V, Z1, norm=cm.colors.LogNorm(), cmap=cm.inferno) #cm.viridis / cm.jet // label='link 1', color='orange'
s1._edgecolors2d = s1._edgecolors3d
s1._facecolors2d = s1._facecolors3d
# s2 = ax.plot_surface(R, V, Z2, label='link 2', color='blue')
# s2._edgecolors2d = s2._edgecolors3d
# s2._facecolors2d = s2._facecolors3d
# s3 = ax.plot_surface(R, V, Z3, label='link 3', color='purple')
# s3._edgecolors2d = s3._edgecolors3d
# s3._facecolors2d = s3._facecolors3d
ax.set_xlabel('Random Num')
ax.set_ylabel('Relative [VEGF]')
ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins='auto', integer=True))

ax.set_zlim(0, 150)
ax.set_zlabel('minimum probability\nrequired to sprout')
plt.legend()
plt.title("1 - ranNum * vegf**link / 10**link")
plt.title('150 * rand / [VEGF]')
plt.show()





# Notes on edge/face color and legend:
# https://stackoverflow.com/questions/55531760/is-there-a-way-to-label-multiple-3d-surfaces-in-matplotlib