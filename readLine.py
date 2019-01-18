from stringIsBlank import isBlank

# -*- coding: utf-8 -*-
"""
Created on Sun May 20 16:04:59 2018

@author: Laine Rumreich

Read in the first non blank line from the given data file and return it.
"""

def readNotBlankLine(dataFile):
    line = dataFile.readline()
    pos = dataFile.tell() # Used to determine if reached EOF to avoid infinite looping
    
    while(isBlank(line) and line is not None):
        line = dataFile.readline()
        
        # Check for EOF
        newpos = dataFile.tell()
        if newpos == pos:  # stream position hasn't changed -> EOF
            return("")
        else:
            pos = newpos
    return(line)