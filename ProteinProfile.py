# Create 3D Plot of Volume restored over time for incremental scaling rates
# Also plots the VEGF over time for incremental scaling rates color coded on the x-y plane
# Control-f for ***** for adjustable inputs / graphing parameters

from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np
import os
import re

os.chdir("..\\TBISimulator\\Output\\")

# Pick param run dir to graph. Example dir: Output_14Day_L0_P9_1NL_10R_1.00V
drugTime = 4320 # *****
dir = "Output_14Day_L0_P8_3MD_150R_1.00A"
dir = f"Output_14Day_L0_Drug{drugTime}_P8_3MD_150R_1.00A" # *****
# Collect time-volume data from ProteinProfile.txt from each run 1 through 17
reParamDir = re.compile("Output_(14)Day_L(\d)_(?:Drug\d+_)*P([89])_3MD_150R_(\d\.\d\d)([AV])")
dirMatches = reParamDir.match(dir)
simTime = dirMatches.group(1)
locationID = dirMatches.group(2)
paramNum = int(dirMatches.group(3))
setScale = float(dirMatches.group(4))
paramLetter = dirMatches.group(5)

inputFileName = "\\Input" + dir[6:] + ".txt"
print("opening file: ", inputFileName)
inputFile = open(dir + inputFileName, 'r')
inputFileContents = inputFile.read()
inputFile.close()

reTime = re.compile("SimulationTime = (\d*\.*\d*)")
simTime = float(reTime.findall(inputFileContents)[0])
reStart = re.compile(("StartParameter = (\d*\.*\d*)"))
startParam = float(reStart.findall(inputFileContents)[0])
reEnd = re.compile(("EndParameter = (\d*\.*\d*)"))
endParam = float(reEnd.findall(inputFileContents)[0])
reRuns = re.compile(("Runs = (\d*\.*\d*)"))
runs = float(reRuns.findall(inputFileContents)[0])
paramStep = (endParam - startParam) / (runs - 1)

days = np.arange(0, simTime * 24 + 1)
dataSetsVolumes = []
dataSetsVEGF = []
dataSetsBound = []
paramValues = np.arange(startParam, endParam + paramStep, paramStep)

run = 1 # *****
variableScale = startParam + (run-1) * paramStep
file = open(dir + "\\Run_" + str(run) + "\\ProteinProfile.txt", 'r')
lines = file.readlines()
file.close()

vegfs = [float(line.split(',')[3].strip()) for line in lines[2:]]
vegfrs = [float(line.split(',')[4].strip()) for line in lines[2:]]
bounds = [float(line.split(',')[5].strip()) for line in lines[2:]]
volumes = [float(line.split(',')[6].strip()) for line in lines[2:]]
vegfGrowthRates = [float(line.split(',')[7].strip()) for line in lines[2:]]
numBisectors = [float(line.split(',')[8].strip()) for line in lines[2:]]

vegfsNormed = [v / vegfs[0] for v in vegfs]
vegfrsNormed = [v / vegfrs[0] for v in vegfrs]
boundsNormed = [b/ bounds[0] for b in bounds]

fig, axVEGF = plt.subplots()
axVEGF.set_xlabel("time [hours]")
axVEGF.set_ylabel("Normalized Concentration")
axVEGF.plot(days, vegfsNormed, label="VEGF")
axVEGF.plot(days, vegfrsNormed, label="VEGFR")
axVEGF.plot(days, boundsNormed, label="VEGFR-VEGF")
plt.legend(loc='center left', bbox_to_anchor=(-10, 11), bbox_transform=axVEGF.transData) # *****
plt.legend(loc=6)

axVolume = axVEGF.twinx()
axVolume._get_lines.prop_cycler = axVEGF._get_lines.prop_cycler
axVolume.set_ylabel("Volume Lost OR  Num Bisectors")
axVolume.plot(days, volumes, label="Volume lost (${mm}^3$)")
axVolume.plot(days, numBisectors, label="Num bisectors")
plt.legend(loc=7) # try 7 or 1

if paramLetter == 'A':
    scaleLabel = "$\gamma_L$ = " + str(variableScale) + " & $\gamma_{on}$ = " + str(setScale)
else:
    scaleLabel = "$\gamma_L$ = " + str(setScale) + " & $\gamma_{on}$ = " + str(variableScale)

drugValue = (run - 1) * paramStep + startParam
plt.title(f"(c): Drug ($\gamma_L$ = {round(drugValue,1)}) applied {drugTime/60/24} days after injury") # *****
plt.title(f"{simTime} Days, Location {locationID}\n{scaleLabel}")
plt.show()

# fig.savefig(f"..\\..\\..\\tbi-documentation\\Publications\\PLoS\\Images\\ProteinProfile_Drug{round(drugValue,1)}_Time{drugTime}.eps", format='eps')