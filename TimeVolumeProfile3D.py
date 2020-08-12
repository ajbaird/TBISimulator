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
drugTime = 4320 # ***** 0, 60, 1440, or 4320
dir = f"Output_14Day_L0_Drug{drugTime}_P8_3MD_150R_1.00A" # *****
dir = "Output_14Day_L0_P8_3MD_150R_1.00A"
# Collect time-volume data from ProteinProfile.txt from each run 1 through 17
reParamDir = re.compile("Output_(14)Day_L(\d)_(?:Drug\w+_)*P([89])_3MD_150R_(\d\.\d\d)([AV])")
dirMatches = reParamDir.match(dir)
simTime = dirMatches.group(1)
locationID = dirMatches.group(2)
paramNum = int(dirMatches.group(3))
setScale = float(dirMatches.group(4))
paramLetter = dirMatches.group(5)

inputFileName = "\\Input" + dir[6:] + ".txt"
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

hours = np.arange(4, simTime * 24 + 1)
dataSetsVolumes = []
dataSetsVEGF = []
dataSetsBound = []
paramValues = np.arange(startParam, endParam + paramStep, paramStep)

runs = range(1,18)
for run in runs:
    file = open(dir + "\\Run_" + str(run) + "\\ProteinProfile.txt", 'r')
    lines = file.readlines()
    file.close()

    vegf = [float(line.split(',')[3].strip()) for line in lines[6:]]
    bound = [float(line.split(',')[5].strip()) for line in lines[6:]]
    volumes = [float(line.split(',')[6].strip()) for line in lines[6:]]
    dataSetsVEGF.append(vegf)
    dataSetsBound.append(bound)
    dataSetsVolumes.append(volumes)

h, p = np.meshgrid(hours, paramValues)
dataSetsVEGF = np.array(dataSetsVEGF)
dataSetsBound = np.array(dataSetsBound)
dataSetsVolumes = np.array(dataSetsVolumes)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_wireframe(h, p, dataSetsVolumes, rstride=1, cstride=25)

myCmap = ax.plot_surface(h, p, dataSetsVEGF, norm=cm.colors.LogNorm(vmin=2e-11, vmax=dataSetsVEGF.max()), cmap=cm.inferno) # Z = dataSetsVEGF or dataSetsVolumes
cbar = plt.colorbar(myCmap)
cbar.set_label("[VEGF]") # "VEGF Concentration" or "Volume Lost"

plt.xlabel("time (hours)")
plt.xticks([4, 168, 336]) # hours[::168]
if paramLetter == 'A':
    titleScale = '$\gamma_{on}$ = ' + str(setScale) + paramLetter
    variableParam = '$\gamma_L$' # 'V'
else:
    titleScale = '$\gamma_L$ = ' + str(setScale) + paramLetter
    variableParam = '$\gamma_{on}$' # 'A'
paramLabel = variableParam
plt.ylabel(paramLabel)
plt.yticks(paramValues[::4])
ax.set_zlabel("Volume lost")

ax.view_init(30, 60) # Set the initial elevation above x-y and azimuthal rotation about z
# plt.title(f"{simTime} Days, Location {locationID}\n{titleScale}")
plt.show()

# fig.savefig(f'..\\..\\..\\tbi-documentation\\Publications\\PLoS\\Images\\Drug{drugTime}_3d.eps', format='eps') # Beware of overwriting
