# Parse Data
# https://www.vipinajayakumar.com/parsing-text-with-python/
# https://docs.python.org/3/library/re.html#re.compile

# Control-f for ***** for adjustable inputs / graphing parameters

# Parameter 8: vary the VEGF growth rate scaling factor
# Parameter 9: vary the association rate scaling factor
# Extract volume restored and number of bisecting nodes for each vegf growth / association rate scaling factor
# Superimpose plots for different locations

# DataPoint class holds {vScale, aScale, volumeGrowth, numBisecting, numSproutNodes (, maxVEGF, maxBound)}
from DataPoint import *

import matplotlib.pyplot as plt
import os
import re

os.chdir("..\\TBISimulator\\Output\\")

reParamDir = re.compile("Output_(14)Day_L(\d)_P(8)_3MD_150R_(1\.00)[AV]")
paramDirs = [dir for dir in os.listdir() if reParamDir.match(dir)]
print(paramDirs)

for dir in paramDirs:
    dataPoints = []

    dirMatches = reParamDir.match(dir)
    simTime = dirMatches.group(1)
    locationID = dirMatches.group(2)
    paramNum = int(dirMatches.group(3))
    setScale = float(dirMatches.group(4))

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
    currentParam = startParam

    runDirs = os.listdir(dir)
    for i in range(1, len(runDirs)):
        filePath = f"{dir}\\Run_{i}\\SummaryFile.txt"

        summaryFile = open(filePath, "r")
        lines = summaryFile.readlines()
        summaryFile.close()

        dataValues = []
        for line in lines:
            value = float(line.split(",")[1].strip())
            dataValues.append(value)

        if paramNum == 8:
            vScale = round(currentParam, 2)
            aScale = setScale
        else: # paramNum == 9
            vScale = setScale
            aScale = round(currentParam, 2)


        # index ~ variable
        # 0 ~ initial volume lost
        # 1 ~ final volumes still lost
        # 2 ~ num bisecting nodes
        # 3 ~ num sprout nodes
        # 4 ~ num active sprout nodes
        # 5 ~ end relative VEGF concentration
        # 6 ~ end relative VEGFR-VEGF concentration
        dataPoint = DataPoint(vScale, aScale, dataValues[0] - dataValues[1], dataValues[2], dataValues[3])
        dataPoints.append(dataPoint)

        currentParam += paramStep

    aValues = [d.aScale for d in dataPoints]
    vValues = [d.vScale for d in dataPoints]
    volumes = [d.volumeGrowth for d in dataPoints]
    bisectors = [d.numBisecting for d in dataPoints]

    locationLabel = "L: " + locationID
    if paramNum == 8:
        plt.plot(vValues, bisectors, label=locationLabel) # pick y = volumes or bisectors *****
        plt.xlabel("$\gamma_L$") # VEGF growth rate scale
    else: # paramNum == 9
        plt.plot(aValues, volumes)
        plt.xlabel("$\gamma_{on}$") # Association rate scale
plt.legend()
plt.ylabel("Num bisectors") # "Volume Restored (${mm}^3$)" or "Num bisectors" *****
plt.title(f"{simTime} Day Run")
plt.show()
