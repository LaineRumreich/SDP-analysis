from analyzeLine import analyzeLine

# -*- coding: utf-8 -*-
"""
Created on Sun May 20 16:07:56 2018

@author: Laine Rumreich

Parse a single data file and record the analyzed data in the variable counts.
"""

# Python imports
from os import remove
import lizard
from shutil import copyfile

# Local imports
from calcCyclomatic import calcCyclomatic
import calcHalstead
from calcMIndex import calcMIndex
       
def parseFile(dataFileName, dataFile, counts): 
    class complexityData:
        inIf = False
        inLoop = False
        nestedLoop = 0 # TODO
        halOperatorList = {} # Halstead complexity metrics data {operator:numOps}
        halOperandList = {} # Halstead complexity metrics data {operand:numOps}
        
    # Analyze each line of the file to populate counts
    line = dataFile.readline()
    while(line):
        analyzeLine(line, dataFile, complexityData, counts) 
        line = dataFile.readline()
    
    # Calculate the cyclomatic complexity data for this file (split into functions)
    filenameDotC = dataFileName[:-4] + ".c"
    copyfile(dataFileName, filenameDotC) # shutil library 
    cyclomaticFunctions = lizard.analyze_file(filenameDotC) # Function complexities
    
    # Calculate overall program cyclomatic complexity
    cyclomaticData = calcCyclomatic(cyclomaticFunctions.function_list, dataFile)
    counts["cyclomatic"] = cyclomaticData[0]
    counts["cyclAvg"] = float("{0:.2f}".format(cyclomaticData[1])) # 2 decimal places
    counts["cyclMed"] = cyclomaticData[2]
    remove(filenameDotC) # Remove the .c file used by the lizard
    
    # Calculate the halstead complexity data for this file based on recorded data
    halstead = calcHalstead.halsteadValues() # Initialize class
    halstead.calcHalstead(complexityData.halOperatorList, complexityData.halOperandList)
    counts["halsteadVolume"] = int(halstead.getVolume())
    counts["halsteadDifficulty"] = float("{0:.2f}".format(halstead.getDifficulty()))
    counts["halsteadEffort"] = int(halstead.getEffort())
    
    # Use the overall program cyclomatic and halstead complexities to determine maintainability index
    maintainability = calcMIndex(counts["lines"], counts["halsteadVolume"], counts["cyclomatic"])
    counts["maintainability"] = float("{0:.2f}".format(maintainability))
