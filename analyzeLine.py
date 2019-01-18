# -*- coding: utf-8 -*-
"""
Created on Sun May 20 16:08:44 2018

@author: Laine Rumreich

Analyze a single line from the input file for complexity and other data.
"""

# Local imports
from stringIsBlank import isBlank
from readLine import readNotBlankLine
from parseFunction import parseFunction
from parseSwitch import parseSwitch
from parseIf import parseIf
from parseLoop import parseLoop
from parseComment import parseComment
from peek import peek
import constants

# Update the Halstead Complexity Operator/Operand List with the current operator
def addOperandToDict(halOpList, token):
        # If the operator has not been seen yet, it has been seen a single time
        numCurrentOp = 1

        # If the operator is already in the dictionary, increment
        if token in halOpList:
            numCurrentOp = halOpList.get(token) + 1

        # Add the operator
        newTuple = {token:numCurrentOp}           
        halOpList.update(newTuple)

# Analyze a single line for the metrics being measured
def analyzeLine(line, dataFile, complexityData, counts): 
    
    # Get rid of blank space at the beginning of the line
    line = line.lstrip()
    
    # Ignore blank lines
    if(isBlank(line)):
        return
    
    ###########################################################################
    #                         General Metrics                                 #
    ###########################################################################
    
    # Count number of lines of comments (blocks count as 1)
    # Then ignore comments
    ifComment = parseComment(line, dataFile, counts)
    if(ifComment):
        # Ignore comments hanging over into the next line 
        if(not any(end in peek(dataFile) for end in constants.END_COMMENTS)):
            line = readNotBlankLine(dataFile)
        return
        
    # Remove any comments at the end of lines
    if(any(c in line for c in constants.COMMENTS)):
        location = line.find("//") 
        line = line[:location] # Remove the comment part of the line
    
    # Number of lines of code (ignores comment only lines)
    counts['lines'] += 1
        
    # Number of time-related functions (tic/toc/pause/sleep/time)
    if any(func in line for func in constants.TIME_FUNCTIONS):
        counts['time'] += 1
        
    # Number of random numbers
    if any(func in line for func in constants.RAND_FUNCTIONS):
        counts['rand'] += 1
        
    # Number of input statements
    if any(ik in line for ik in constants.INPUT_KEYWORDS):
        counts['input'] += 1
        
    # Number of plotting statements
    if any(func in line for func in constants.PLOT_FUNCTIONS):
        counts['plot'] += 1
        
    # Number of print statements
    if(any(pk in line for pk in constants.PRINT_KEYWORDS) and not any(pk in line for pk in constants.NOT_PRINT_KEYWORDS)):
        counts['print'] += 1
            
    # Return if any print keywords in line to avoid finding looping and 
    # conditional keywords that are in print statements
    if (any(wk in line for wk in constants.WRITE_KEYWORDS) and "}" not in line):
        return
    
    ###########################################################################
    #                           Halstead Metrics                              #
    ###########################################################################
        
    tokens = line.split(" ")
    
    # Split tokens into operators and operands
    index = 0
    while index < len(tokens):
        token = tokens[index]
        # Ignore preprocessor directive lines
        if constants.PRE_DIRECTIVES.__contains__(token):
            break
        
        # Check for non-mathematical operators (ex. reserved words, storage identifiers)
        if constants.OPERATORS.__contains__(token):
            addOperandToDict(complexityData.halOperatorList, token)
        else:
            # Check for mathematical operators (ex. <=, {}, &, ;)
            for op in constants.OPERATOR:
                if op in token:
                    
                    # Add the operator to the dictionary
                    addOperandToDict(complexityData.halOperatorList, op)
                    
                    # Remove the token
                    # Continue analyzing anything before it
                    # Add anything after it back into tokens
                    opIndex = token.find(op)
                    if(len(token) > opIndex + len(op)):
                        tokens.append(token[opIndex+len(op):])
                    token = token[:opIndex]
                    
            # Do not count ),},] operators on their own, but not included in operand
            token = token.replace(")", '') 
            token = token.replace("}", '')
            token = token.replace("]", '')
    
            # Add what is left of the token to operand
            if(not isBlank(token)):
                addOperandToDict(complexityData.halOperandList, token.strip())
                
        index += 1

    ###########################################################################
    #                          Complex Metrics                                #
    ###########################################################################
    
    # If entering main function, parse it as a function
    if("int main(" in line):
        parseFunction(line, dataFile, complexityData, counts)
            
    # Number of user defined functions *look for type, (), and {*            
    if(any(f in line for f in constants.FUNCTION_KEYWORDS) and "(" in line and not any(nf in line for nf in constants.NOT_FUNCTION_KEYWORDS)):
        if ("{" in line or "{" in peek(dataFile)):
            counts['userFunc'] += 1
            parseFunction(line, dataFile, complexityData, counts)
                  
    # Number of for loops
    if (any(wk in line for wk in constants.FOR_KEYWORDS)):
        counts['forLoops'] += 1
        # Continue parsing the file from in parseLoop until the correct "}" is found
        if(complexityData.inLoop): # If already in a loop, increment nestedLoop
            counts['nestedLoops'] += 1
            parseLoop(dataFile, complexityData, counts)
        else:
            complexityData.inLoop = True
            parseLoop(dataFile, complexityData, counts)
            complexityData.inLoop = False
                
    # Number of while loops
    if(any(dk in line for dk in constants.DO_KEYWORDS)): 
        # Do not increment here; instead increment when "while();" is found
        # Continue parsing the file from parseLoop until the correct "}" is found
        if(complexityData.inLoop): # If already in a loop, increment nestedLoop
            counts['nestedLoops'] += 1
            if('}' not in line and ';' not in line):    # Make sure it is not an empty block
                parseLoop(dataFile, complexityData, counts)
        else:
            complexityData.inLoop = True
            if('}' not in line and ';' not in line):    # Make sure it is not an empty block
                 parseLoop(dataFile, complexityData, counts)
            complexityData.inLoop = False
    if(any(wk in line for wk in constants.WHILE_KEYWORDS)):
        counts['whileLoops'] += 1
        # Continue parsing the file from parseLoop until the correct "}" is found
        if(complexityData.inLoop): # If already in a loop, increment nestedLoop
            counts['nestedLoops'] += 1
            if('}' not in line and ';' not in line):    # Make sure it is not an empty block
                parseLoop(dataFile, complexityData, counts)
        else:
            complexityData.inLoop = True
            if('}' not in line and ';' not in line):    # Make sure it is not an empty block
                 parseLoop(dataFile, complexityData, counts)
            complexityData.inLoop = False
     
    # Number of if statements   
    if(((any(wk in line for wk in constants.IF_KEYWORDS)) and "else" not in line) and "else" not in peek(dataFile)):
        counts['ifElse'] += 1
        # Continue parsing the file from parseIf until the correct "}" is found
        if(complexityData.inIf): # If already in a conditional, increment nestedIf
            counts['nestedIfs'] += 1
            if("}" not in line and ';' not in line): # avoid infinite looping if empty block
                parseIf(dataFile, complexityData, counts)
        else:
            complexityData.inIf = True
            if("}" not in line and ';' not in line): # avoid infinite looping if empty block
                parseIf(dataFile, complexityData, counts)
            complexityData.inIf = False 
         
    if("else" in line): # Parse any else ifs or elses as if statements, but do not add to total num ifs
        # Continue parsing the file from parseIf until the correct "}" is found
        if(complexityData.inIf):
            if("}" not in line): # avoid infinite looping if empty block
                # Check to make sure the next line does not say "if", which 
                # would cause a recursive call that would mess up "}"
                secondElseLine = readNotBlankLine(dataFile)
                if(not any(wk in secondElseLine for wk in constants.IF_KEYWORDS) ):
                    analyzeLine(secondElseLine, dataFile, complexityData, counts) 
                if("}" not in secondElseLine):
                    parseIf(dataFile, complexityData, counts)
        else:
            complexityData.inIf = True
            if("}" not in line): # avoid infinite looping if empty block
                # Check to make sure the next line does not say "if", which 
                # would cause a recursive call that would mess up "}"
                secondElseLine = readNotBlankLine(dataFile)
                if(not any(wk in secondElseLine for wk in constants.IF_KEYWORDS) ):
                    analyzeLine(secondElseLine, dataFile, complexityData, counts)  
                if("}" not in secondElseLine):
                    parseIf(dataFile, complexityData, counts)
            complexityData.inIf = False
                
    # Number of switch cases
    if(any(s in line for s in constants.SWITCH_KEYWORDS)): 
        counts['switch'] += 1 
        # Continue parsing the file from parseSwitch until the correct "}" is found
        parseSwitch(dataFile, complexityData, counts)   
            