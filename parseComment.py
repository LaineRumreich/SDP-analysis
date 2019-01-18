from stringIsBlank import isBlank

# -*- coding: utf-8 -*-
"""
Created on Sun May 20 17:10:29 2018

@author: Laine Rumreich

Count number of lines of comments (blocks count as 1), then remove the comments 
from input lines.
"""
# Local imports
import constants
from peek  import peek


def parseComment(line, dataFile, counts):
    if(any(c in line for c in constants.COMMENTS)):
        if("/*" in line and "//" not in line):
            counts['comments'] += 1
            while("*/" not in line):
                line = dataFile.readline()
        
        # Check if the comment is its own line or part of another line of code
        location = line.find("//") 
        
        # Only count blocks of comments once
        if(location != 0 or peek(dataFile)[0] is not '/'):
            counts['comments'] += 1
            
        line = line[:location] # Remove the comment part of the line
        if(isBlank(line)): # Return if the entire line was a comment
            return True
        
    return False # entire line was not a comment
    