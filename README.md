# Traumatic Brain Injury Project 
Traumatic brain injury effects millions of Americans each year. In addition to the immediate injury concerns, patients afflicted with a TBI have the potential for long term debilitating damage. Although a good amount of research and understanding has been established regarding the moment of impact and tissue damage therein, many modeling efforts have not addressed patient physiology beyond the milisecond time scale. Due to recent breakthroughs in TBI recovery understanding, it is becoming more and more clear that therapuetic interventions over the course of days to weeks may create significant long term positive outcomes in a patients recovery. We seek to create a mathematical model that is able to simulate the patient's angiogensis over these time scales. We explore the role that protein interactions have on global microvascular growth and overall restoration of blood flow to the damaged tissue region.

## Technical Details

The TBI project is written and built in C++ and may be run in a windows environment. Output files will generate all data used in any upcoming publications. To run a given output file download the zipped release data, unzip the data then navigate to the folder with the file TBISimulator.exe, then from the command line type ```./TBISimulator.exe Input_Files/Inputs_For_All_Data/Input_14Day_L0_Drug60_P8_3MD_150R_1.00A.txt```

This command will run the given configuration file. For details see our upcoming publication.

## Accessing the Executable
The the code base is pre-built for the Windows platform and available in the releases tab. Navigate to that window in github ([here](https://github.com/ajbaird/TBISimulator/releases/tag/v0.1)).
To run the executable download the zip file, unzip the x64-Release.zip file, and navigate to the following folder: 

- `x64-Release/`
   - `Input_Files/` 
	
From this folder, open a command line window and type  ```.././TBISimulator.exe Input_Files/Inputs_For_All_Data/Input_14Day_L0_Drug60_P8_3MD_150R_1.00A.txt```. This should run the .txt executable file the game. If you have issues please contact: abaird@ara.com.

Programmatics
===============
The multiscale TBI project is funded under contract number: W911NF-17-1-0572  

Disclaimer:

This work is supported by the Army Research Labs. The views, opinions and/or findings contained in this report are those of the author(s) and should not be construed as an official Department of the Army position, policy, or decision unless so designated by other documentation.

DOI and Refs
===============
[![DOI](https://zenodo.org/badge/287111993.svg)](https://zenodo.org/badge/latestdoi/287111993)




