# -*- coding: utf-8 -*-
"""
Created on Sun May 20 16:42:51 2018

@author: Laine Rumreich

Parse the entire current switch case.
"""

def parseSwitch(dataFile, complexityData, counts):
    from analyzeLine import analyzeLine
    line = dataFile.readline()
    # Quit when the current switch case ends
    while('}' not in line):
        analyzeLine(line, dataFile, complexityData, counts)
        line = dataFile.readline()
        
    # Analyze the line with "}" in it
    analyzeLine(line, dataFile, complexityData, counts)