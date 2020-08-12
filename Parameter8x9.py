## 3D plot of volume restored across a matrix of VEGF growth and associate rate scaling factors (0.2 to 1.8 in increments of 0.1)

# Control-f for ***** for adjustable inputs / graphing parameters

# Link degrees are set to 1 (linear): 1NL
# Random number multiplier is set to 10: 10R
# Parameter 8 = VEGF scaling factor. *Set this as the Parameter in the input file
# Parameter 9 = Association rate scaling factor. *Set a specific value for the association rate in the input value
# Parameter 8 was varied with each run, for where parameter 9 was constant in a set of runs
#     and incrementally increased across sets of runs

from DataPoint import *

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from operator import attrgetter
import os
import re

os.chdir("..\\TBISimulator\\Output\\")

# Example dir: Output_P8_1NL_90R_0.2A
# All output dirs processed by this .py file follow naming scheme:
# Output_P[parameter number]_[degree of new sprout link]NL_[random number multiplier]R_[association rate scaling factor]A
fig = plt.figure()
locs = range(1,5) # range(0,6)# *****
for loc in locs:
    reString = f"Output_(14)Day_L({loc})_P8_3MD_150R_(\d\.\d\d)A"
    reP8x9Dir = re.compile(reString)
    paramDirs = os.listdir()
    paramDirs[:] = [dir for dir in paramDirs if reP8x9Dir.match(dir)]
    print(paramDirs, "\n")

    dataPoints = []
    for dir in paramDirs:
        matches = reP8x9Dir.match(dir)
        # Group 0 is the dir
        simTime = matches.group(1)
        locationID = matches.group(2)
        aScale = float(matches.group(3))

        inputFileName = "\\Input" + dir[6:] + ".txt"

        inputFile = open(dir + inputFileName, 'r')
        inputFileContents = inputFile.read()
        inputFile.close()
        reStart = re.compile(("StartParameter = (\d*\.*\d*)"))
        startParam = float(reStart.findall(inputFileContents)[0])
        reEnd = re.compile(("EndParameter = (\d*\.*\d*)"))
        endParam = float(reEnd.findall(inputFileContents)[0])
        reRuns = re.compile(("Runs = (\d*\.*\d*)"))
        runs = float(reRuns.findall(inputFileContents)[0])
        paramStep = (endParam - startParam) / (runs - 1)
        vScale = startParam

        runDirs = os.listdir(dir)
        for i in range(1, len(runDirs)): # ignore the input parameter file
            filePath = dir + "\\Run_" + str(i) + "\\SummaryFile.txt"

            summaryFile = open(filePath, "r")
            lines = summaryFile.readlines()
            summaryFile.close()

            dataValues = []
            # index ~ variable
            # 0 ~ initial volume lost
            # 1 ~ final volumes still lost
            # 2 ~ num bisecting nodes
            # 3 ~ num sprout nodes
            # 4 ~ num active sprout nodes
            # 5 ~ end relative VEGF concentration
            # 6 ~ end relative VEGFR-VEGF concentration
            for line in lines:
                value = float(line.split(",")[1].strip())
                dataValues.append(round(value, 2))

            point = DataPoint(vScale, aScale, dataValues[0] - dataValues[1], dataValues[2], dataValues[3])

            # Find max VEGF from the run
            filePath = dir + "\\Run_" + str(i) + "\\ProteinProfile.txt"
            summaryFile = open(filePath, "r")
            lines = summaryFile.readlines()
            summaryFile.close()

            maxVEGF = max([float(line.split(',')[3].strip()) for line in lines[1:]])
            maxBound = max([float(line.split(',')[5].strip()) for line in lines[1:]])
            point.SetMaxVEGF(maxVEGF)
            point.SetMaxBound(maxBound)
            dataPoints.append(point)

            vScale += paramStep

    # for d in dataPoints:
    #     d.Print()

    dataPoints.sort(key=attrgetter('aScale', 'vScale'))

    aScales = [d.aScale for d in dataPoints]
    vScales = [d.vScale for d in dataPoints]
    # volumes = [d.volumeGrowth for d in dataPoints]

    aSet = sorted(set(aScales)) # Remove duplicates and sort the various aScale values
    vSet = sorted(set(vScales)) # Remove duplicates and sort the various vScale values
    A, V = np.meshgrid(aSet, vSet)

    Volume = [[0 for i in range(len(aSet))] for j in range(len(vSet))]
    VEGF = [[0 for i in range(len(aSet))] for j in range(len(vSet))]
    Bound = [[0 for i in range(len(aSet))] for j in range(len(vSet))]
    for d in dataPoints:
        a = d.aScale
        v = d.vScale
        indexA = aSet.index(a)
        indexV = vSet.index(v)
        Volume[round(indexV)][round(indexA)] = d.volumeGrowth # Pick d.numBisecting or d.volumeGrowth *****
        VEGF[round(indexV)][round(indexA)] = d.maxVEGF
        Bound[round(indexV)][round(indexA)] = d.maxBound

    Volume = np.array(Volume)
    VEGF = np.array(VEGF)
    Bound = np.array(Bound)

    # https://medium.com/@sebastiannorena/3d-plotting-in-python-b0dc1c2e5e38
    # fig = plt.figure() # Uncomment for single plot *
    # ax = plt.axes(projection='3d') # Uncomment for Single plot *
    ax = fig.add_subplot(2, 2, loc, projection='3d') # or add_subplot(2, 3, loc + 1, ...) or 2, 2, loc, *****
    #ax.plot_wireframe(A, V, Volume, color='orange')
    # volume: vmin = 0, vmax = 300. num bisecting: vmin=10, vmax=50 *****
    vMin = 1
    vMax = 85
    myCmap = ax.plot_surface(A, V, Volume, cmap=cm.viridis, norm=cm.colors.LogNorm(vmin=vMin, vmax=vMax))
    # cbar = plt.colorbar(myCmap)
    ax.set_xlabel('$\gamma_{on}$') # A scale
    plt.xticks(np.arange(0.2, round(aSet[-1],1)+0.2, 0.8))
    ax.set_ylabel('$\gamma_L$') # V scale
    plt.yticks(np.arange(0.2, round(vSet[-1],1)+0.2, 0.8))
    # Pick and un/comment: Volume Regrown / Num Bisecting *****
    # cbar.set_label('Volume Regrown')
    ax.set_zlabel('Volume Regrown')
    # cbar.set_label('Num Bisecting')
    # ax.set_zlabel('Num Bisecting')

    # Uncomment below and adjust above to plot VEGF or Bound colorcoded on the x-y plane
    # myCmap = ax.plot_surface(A, V, VEGF, norm=cm.colors.LogNorm(vmin=VEGF.min(), vmax=VEGF.max()), cmap=cm.viridis)
    # # myCmap = cm.ScalarMappable(cmap=cm.viridis)
    # # myCmap.set_array(VEGF) # update here too: VEGF or Bound
    # cbar = plt.colorbar(myCmap)
    # cbar.set_label('VEGF concentration')
    # ticks1 = np.round(np.linspace(VEGF.min(), 10 ** -9, 10), 10)
    # ticks2 = np.round(np.linspace(10**-9, VEGF.max(), 10), 9)
    # ticks = np.concatenate((ticks1, ticks2))
    # ticks = np.unique(ticks)
    # cbar.set_ticks(ticks)
    # cbar.set_ticklabels(ticks)
    # cbar.update_ticks()
    plt.title("Location " + locationID)
    ax.zaxis.set_major_locator(ticker.MaxNLocator(nbins='auto', integer=True))
    ax.view_init(20, 230) # Set the initial elevation above x-y and azimuthal rotation about z

fig.subplots_adjust(right=0.8)
ax_cbar = fig.add_axes([0.85, .1, .02, .8]) # [x pos, y pos, width, height]
cbar = fig.colorbar(myCmap, cax=ax_cbar, format='%d')
cbar.set_label('Volume Regrown')
ticks = [vMin, round(vMax*0.1), int(round(vMax*0.5, -1)), vMax]
cbar.set_ticks(ticks)
cbar.set_ticklabels(ticks)
cbar.update_ticks()

# fig.suptitle(simTime + " Day Simulation")

plt.show()
