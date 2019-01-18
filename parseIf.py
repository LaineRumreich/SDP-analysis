# -*- coding: utf-8 -*-
"""
Created on Sun May 20 16:43:35 2018

@author: Laine Rumreich

Parse the entire current conditional.
"""
# Local imports
from readLine import readNotBlankLine
import constants

comments = ["//"]

def checkComments(line):
    if(any(c in line for c in comments)):
        location = line.find("//")
        return(line[:location])
    else:
        return(line)

def parseIf(dataFile, complexityData, counts):
    from analyzeLine import analyzeLine
    line = dataFile.readline()
    # Quit when the current conditional ends
    while('}' not in line):
        analyzeLine(line, dataFile, complexityData, counts)        
        line = dataFile.readline()
      
    nonCommentLine = checkComments(line) # Check that the word "else" is not within a comment
    if("else" in nonCommentLine): # Check for any else ifs or elses after '}'s
        if("}" not in line): # avoid infinite looping if empty block
            # Check to make sure the next line does not say "if", which 
            # would cause a recursive call that would mess up "}"
            secondElseLine = readNotBlankLine(dataFile)
            if( not any(wk in secondElseLine for wk in constants.IF_KEYWORDS) ):
                analyzeLine(line, dataFile, complexityData, counts)
            if("}" not in secondElseLine):
                parseIf(complexityData, dataFile, counts)