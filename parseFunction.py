# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 23:08:35 2018

@author: Laine Rumreich

Parse the entire current function. This includes the main function.
"""

def parseFunction(line, dataFile, complexityData, counts):
    from analyzeLine import analyzeLine
    
    # Parse the entire function and quit when the current loop ends
    line = dataFile.readline()
    while('}' not in line):
        analyzeLine(line, dataFile, complexityData, counts)
        line = dataFile.readline()
        
    # Analyze the line with "}" in it
    analyzeLine(line, dataFile, complexityData, counts)
    
