# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 14:06:36 2018

@author: Laine Rumreich

Look at the next or previous (non blank) line in a file without advancing readline().
"""
# Local imports
from readLine import readNotBlankLine

def peekNotBlank(dataFile):
    pos = dataFile.tell() # Get the current position
    line = readNotBlankLine(dataFile)
    dataFile.seek(pos) # Return to the original position in the file
    return line

def peek(dataFile):
    pos = dataFile.tell() # Get the current position
    line = dataFile.readline()
    dataFile.seek(pos) # Return to the original position in the file
    return line