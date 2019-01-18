# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 21:35:50 2018

@author: Laine Rumreich

Program to determine the Cyclomatic Complexity of a Software Design Project. 
Note that this file computes the complexity based on the complexities of each
function in the current SDP. In addition, the mean and median cyclomatic 
complexities of the functions in the file are calculated.

General Information (Microsoft):
    Higher numbers are considered “bad” and lower numbers are “good”. It is 
    used to get a sense of how hard any given code may be to test, maintain, or 
    troubleshoot as well as an indication of how likely the code will be to 
    produce errors. At a high level, the value of cyclomatic complexity is 
    determined by counting the number of decisions made in the source code.

Formula (Microsoft):
    cyclomatic complexity = the number of edges - the number of nodes + 1
    
    where a node represents a logic branch point and an edge represents a 
    line between nodes.
    
Notes:
    Since many SDPs are organized using user defined functions, the cyclomatic
    complexities of the entire current SDP is determined by 
        ∑[(function compexity - 1) * number of function calls] + main complexity
        
    This value is calculated based on what the complexity would be if the program
    were written as one long main program rather than calling additional functions.
"""

# Python imports
import statistics

# Local imports
from timesCalled import timesCalled

def calcCyclomatic(cyclomaticFunctions, dataFile):
    cyclComplexity = 0
    cyclAvg = 0
    cyclMedian = 0
    cyclValues = []
    numFuncs = max(1,len(cyclomaticFunctions))

    while len(cyclomaticFunctions) > 0:
        currentFunc = cyclomaticFunctions.pop(0)
        currentTimesCalled = timesCalled(currentFunc.name, dataFile)
        currentFuncComplexity = currentFunc.cyclomatic_complexity - 1
        cyclComplexity += currentTimesCalled * currentFuncComplexity
        cyclAvg += currentFuncComplexity
        cyclValues.append(currentFuncComplexity)
        
    cyclAvg /=  numFuncs
    
    if len(cyclValues) != 0:
        cyclMedian = statistics.median(cyclValues)
        
    return [cyclComplexity, cyclAvg, cyclMedian]
        
        