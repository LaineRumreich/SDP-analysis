# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 18:59:11 2018

@author: Laine Rumreich

Determines how many times a function is called in a file without advancing readline().
"""

# Local imports
import constants

def timesCalled(funcName, dataFile):
    pos = dataFile.tell() # Get the current position
    timesCalled = 0
    dataFile.seek(0) # Return to the initial position in the file
    
    # Parse through the entire file to find function calls
    line = dataFile.readline()
    while(line):
        if(funcName + "(" in line or funcName + " (" in line):
            # If constructor or prototype, skip
            if(("{" not in line or "if" in line) and (not any(c in line for c in constants.TYPE_KEYWORDS) or "print" in line)):
                timesCalled += 1
        line = dataFile.readline()
    if(funcName == "main"):
        timesCalled = 1 # main should never be explicitly called but runs exactly once
        
    dataFile.seek(pos) # Return to the original position in the file
    return max(1, timesCalled) # Assume each function is called at least once

