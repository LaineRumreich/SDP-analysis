# -*- coding: utf-8 -*-
"""
Created on Sun May 20 14:12:00 2018

@author: Laine Rumreich

Print out the final output to the output data excel file.
"""

def printOutput(output, lineNum, counts):
    lineString = "B"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['lines']
    
    lineString = "C"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['comments']
    
    lineString = "D"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['forLoops']
    
    lineString = "E"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['whileLoops']
    
    lineString = "F"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['nestedLoops']
    
    lineString = "G"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['highestNestedLoop']
    
    lineString = "H"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['ifElse']
    
    lineString = "I"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['nestedIfs']
    
    lineString = "J"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['time']
    
    lineString = "K"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['rand']
    
    lineString = "L"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['input']
    
    lineString = "M"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['plot']
    
    lineString = "N"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['print']
    
    lineString = "O"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['switch']
    
    lineString = "P"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['cyclomatic']
    
    lineString = "Q"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['cyclAvg']
    
    lineString = "R"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['cyclMed']
    
    lineString = "S"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['halsteadVolume']
    
    lineString = "T"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['halsteadDifficulty']
    
    lineString = "U"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['halsteadEffort']
    
    lineString = "V"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['maintainability']
    
    lineString = "W"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['userFunc']
    
    lineString = "X"
    lineString = lineString + str(lineNum)
    output[lineString] = counts['addFunc']
    
    