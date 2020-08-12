import os

dataParseDir = os.getcwd()
# "..\\..\..\\Fall Internship\\Old Data\\Data - pre dt units adjustment"
os.chdir("..\\TBISimulator\\Input_Files\\Inputs_For_All_Data\\LRR13")

dirs = [dir for dir in os.listdir() if dir.split("_")[1] == "14Day"]

for dir in dirs:
    sourceFile = dir #+ "\\Run_1\\parameters20.txt"
    fileIn = open(sourceFile, 'r')
    lines = fileIn.readlines()
    fileIn.close()

    #lines[14:16] = ["SproutingRandNumMultiplier = 150\n", "MinDistanceBetweenSprouts = 3.0\n"]
    lines[0] = "LengthRadiusRatio = 20\n"
    #lines[9] = "SimulationTime = 14.0\n"
    paramSpecs = dir.split('_')
    # newFileName = "Input_14Day"
    # for spec in paramSpecs[2:4]:
    #     newFileName+= '_' + spec
    # newFileName+='_3MD_150R'
    # for spec in paramSpecs[6:]:
    #     newFileName+= '_' + spec

    # newFileName+=".txt"
    #fileOut = open(dataParseDir + "\\..\\TBISimulator\\Input_Files\\Inputs_For_All_Data\\" + newFileName, 'w')
    fileOut = open("..\\..\\Inputs_For_All_Data\\" + sourceFile, 'w')
    fileOut.writelines(lines)
    fileOut.close()

