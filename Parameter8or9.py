# Parse Data
# https://www.vipinajayakumar.com/parsing-text-with-python/
# https://docs.python.org/3/library/re.html#re.compile

# Control-f for ***** for adjustable inputs / graphing parameters

# Parameter 8: vary the VEGF growth rate scaling factor
# Parameter 9: vary the association rate scaling factor
# Extract volume restored and number of bisecting nodes for each vegf growth / association rate scaling factor
# Plot extended range of a/v Scales by appending datasets from parameter runs

# DataPoint class holds {vScale, aScale, volumeGrowth, numBisecting, numSproutNodes (, maxVEGF, maxBound)}
from DataPoint import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import re

os.chdir("..\\TBISimulator\\Output\\Output")

# Example dirs: Output_7Day_L0_P8[a-c]_1NL_10R_1.00A
reParamDir = re.compile("Output_(14)Day_L(0)_P(8)\w_3MD_150R_(1\.00)[AV]") # P(8) or P(9) *****
paramDirs = [dir for dir in os.listdir() if reParamDir.match(dir)]
print(paramDirs)

dataPoints = []
fig, axVolume = plt.subplots()
axBisectors = axVolume.twinx() # Comment out if only plotting Volumes OR Num Bisectors *****
for dir in paramDirs:
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

        if paramNum == 9:
            vScale = setScale
            aScale = round(currentParam, 2)
        else: # paramNum == 8
            vScale = round(currentParam, 2)
            aScale = setScale

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

    axVolume.set_ylabel("Volume Restored")
    if True: # Overlay volumes and bisectors plots
        axVolume.set_ylabel("Volume Restored", color='blue')
        axBisectors.set_ylabel("Num Bisectors", color='orange')
        axBisectors.yaxis.set_major_locator(ticker.MaxNLocator(nbins='auto', integer=True))
        if paramNum == 8:
            axVolume.plot(vValues, volumes, label='Volumes', color='blue')
            axBisectors.plot(vValues, bisectors, label='Bisectors', color='orange')
            axVolume.set_xlabel("$\gamma_L$") # VEGF Growth Rate Scaling Factor

        else:  # paramNum == 9
            axVolume.plot(aValues, volumes, label='Volumes', color='blue')
            axBisectors.plot(aValues, bisectors, label='Bisectors', color='orange')
            axVolume.set_xlabel("$\gamma_{on}$") # Association Rate Scaling Factor
    elif True: # plot only volumes
        if paramNum == 8:
            axVolume.plot(vValues, volumes)
            axVolume.set_xlabel("VEGF Growth Rate Scaling Factor")

        else:  # paramNum == 9
            axVolume.plot(aValues, volumes)
            axVolume.set_xlabel("Association Rate Scaling Factor")
    else: # plot only bisectors
        if paramNum == 8:
            axVolume.plot(vValues, bisectors)
            axVolume.set_xlabel("VEGF Growth Rate Scaling Factor")

        else:  # paramNum == 9
            axVolume.plot(aValues, bisectors)
            axVolume.set_xlabel("Association Rate Scaling Factor")

# plt.title(f'{simTime} Day Run, Location {locationID}')
plt.show()
