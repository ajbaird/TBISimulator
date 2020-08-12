# Examine new sprout formation sensitivity to degree of VEGFR-VEGF link and Random Number Multiplier (RNM)
# Result variable: number of bisecting nodes
# independent variables: link degree (^0 to ^4) and RNM

import matplotlib.pyplot as plt
from matplotlib import cm
import os
import re
from operator import attrgetter


class DataPoint:
    """Stores a and VEGF scaling rates, and resulting end volume from that 7 day simulation run"""

    def __init__(self, linkDegree, rnm, vScale, numBisecting, volumeGrowth, numSproutNodes):
        self.linkDegree = linkDegree
        self.rnm = rnm
        self.vScale = vScale
        self.volumeGrowth = volumeGrowth
        self.numBisecting = numBisecting
        self.numSprouts = numSproutNodes

    def Print(self):
        print("Link: {0.linkDegree}, RNM: {0.rnm}, # Bisecting: {0.numBisecting}, # Sprouts: {0.numSprouts}, Volume Growth: {0.volumeGrowth}".format(self))


os.chdir("..\\TBISimulator\\Output\\")
paramDirs = os.listdir()
# Example dir: Output_P9_1NL_90R
# All output dirs start with Output_P[parameter number]

print(paramDirs, "\n")

paramDirs[:] = [dir for dir in paramDirs if dir.split('_')[0] == "Output"]

print(paramDirs)

filePaths = []
dataPoints = []
for dir in paramDirs:
    if dir.split('_')[1] == "P6":
        reBigDir = re.compile('Output_P\d_(\d.\d)V_(\d+)R')
        matches = reBigDir.match(dir)
        # Group 0 is the dir
        vScale = float(matches.group(1))
        rnm = int(matches.group(2))

        runDirs = os.listdir(dir)
        for i in range(1, len(runDirs) + 1):
            filePath = dir + "\\Run_" + str(i) + "\\SummaryFile.txt"
            filePaths.append(filePath)

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
                dataValues.append(value)

            dataPoints.append(
                DataPoint(i - 1, rnm, vScale, dataValues[2], dataValues[0] - dataValues[1], dataValues[3]))

dataPoints.sort(key=attrgetter('vScale', 'rnm', 'linkDegree'))

rnm_values = [d.rnm for d in dataPoints]
num_bisecting = [d.numBisecting for d in dataPoints]
link_degrees = [d.linkDegree for d in dataPoints]

# https://stackoverflow.com/questions/10761429/how-to-modify-2d-scatterplot-to-display-color-based-off-third-array-in-csv-file
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('random num')
ax.set_ylabel('link degree')
s = ax.scatter(rnm_values, link_degrees, c=num_bisecting, marker='o', cmap=cm.jet)
plt.colorbar(s)
plt.show()

diffedVEGF = []
halfData = int(len(dataPoints) / 2)
for i in range(halfData):
    diffedVEGF.append(dataPoints[i + halfData].volumeGrowth - dataPoints[i].volumeGrowth)  ## change key as desired

fig2 = plt.figure()
subPlot = fig2.add_subplot(111)
subPlot.set_title('volume colored')
subPlot.set_xlabel('random num')
subPlot.set_ylabel('linkDegree')
scat = subPlot.scatter(rnm_values[:halfData], link_degrees[:halfData], c=diffedVEGF, marker='o', cmap=cm.jet)
plt.colorbar(scat)
plt.show()