# Create 2D plot of volume lost over time
# *****: Use these lines if you want to specify which directories and which runs within those directories.
    # Either move below the duplicate variable / command, or uncomment. Comment the duplicate variable / command.

import matplotlib.pyplot as plt
import os
import re

os.chdir("..\\TBISimulator\\Output\\")

# Pick dirs to graph. Example dir: Output_14Day_L0_P8_1NL_10R_1.00A
reParamDir = re.compile(r"Output_(14)Day_L(\d)_P([89])_3MD_150R_(\d\.\d*)([AV])\\Run_(\d+)") # *****
# reParamDir = re.compile("Output_(14)Day_L(0)_P([89])_3MD_150R_(1\.00)([AV])")
dirs = [dir for dir in os.listdir() if reParamDir.match(dir)] # *****
dirs = ["Output_14Day_L0_P8_3MD_150R_1.00A\\Run_7", "Output_14Day_L1_P8_3MD_150R_1.20A\\Run_5",
        "Output_14Day_L2_P8_3MD_150R_1.00A\\Run_16", "Output_14Day_L3_P8_3MD_150R_1.80A\\Run_17",
        "Output_14Day_L4_P8_3MD_150R_1.80A\\Run_17", "Output_14Day_L5_P8_3MD_150R_1.80A\\Run_17"] # *****
dirs = ["Output_14Day_L0_P8_3MD_150R_1.00A\\Run_9", "Output_14Day_L1_P8_3MD_150R_1.00A\\Run_9",
        "Output_14Day_L2_P8_3MD_150R_1.00A\\Run_9", "Output_14Day_L3_P8_3MD_150R_1.00A\\Run_9",
        "Output_14Day_L4_P8_3MD_150R_1.00A\\Run_9", "Output_14Day_L5_P8_3MD_150R_1.00A\\Run_9"] # *****

dataSetsDays = []
dataSetsVolumes = []
dataSetsVScales = []
dataSetsAScales = []
dataSetsLocationIDs = []
dataSetsRun = []
# Collect time-volume data from ProteinProfile.txt from each run 1, 9, 17
for dir in dirs:
    matches = reParamDir.match(dir)
    simTime = matches.group(1)
    locationID = matches.group(2)
    dataSetsLocationIDs.append(locationID)
    paramNum = int(matches.group(3))
    setScale = float(matches.group(4))
    paramLetter = matches.group(5)
    runNum = int(matches.group(6)) # *****

    inputFileName = "\\Input" + dir[6:] + ".txt"
    inputFileName = "\\..\\Input" + dir[6:].split('\\')[0] + ".txt" # *****
    #inputFile = open(dir + inputFileName, 'r') # *****
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

    runs = [1, 2, 3, 4, 9, 17]
    runs = [runNum] # *****
    for run in runs:
        if paramLetter == 'V':
            dataSetsVScales.append(setScale)
            dataSetsAScales.append(round(startParam + paramStep * (run - 1), 2))
        elif paramLetter == 'A':
            dataSetsVScales.append(round(startParam + paramStep * (run - 1), 2))
            dataSetsAScales.append(setScale)

        # file = open(f"{dir}\\Run_{run}\\ProteinProfile.txt", 'r')
        file = open(f"{dir}\\ProteinProfile.txt", 'r') # *****
        lines = file.readlines()
        file.close()
        days = [float(line.split(',')[1].strip()) for line in lines[2:]]
        dataSetsDays.append(days)
        volumes = [float(line.split(',')[6].strip()) for line in lines[2:]]
        dataSetsVolumes.append(volumes)

fig = plt.figure()
for i in range(len(dataSetsVolumes)):
    latexV = "$\gamma_L$"
    latexA = "$\gamma_{on}$"
    paramLabel = f"V: {dataSetsVScales[i]}, A: {dataSetsAScales[i]}"
    paramLabel = f"Loc: {dataSetsLocationIDs[i]}, {latexV}={dataSetsVScales[i]}, {latexA}={dataSetsAScales[i]}" # *****
    if i!= -1:
        plt.plot(dataSetsDays[i][4:], dataSetsVolumes[i][4:], label=paramLabel)
    else: # *****
        plt.plot(dataSetsDays[i][4:], dataSetsVolumes[i][4:])

plt.xlabel("time (hours)")
plt.ylabel("Volume lost")
plt.legend()
# plt.title(f"{simTime} Days, Location {locationID}")
# plt.title(f"{simTime} Days") # *****
plt.show()
