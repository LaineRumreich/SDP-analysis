# -*- coding: utf-8 -*-
"""
Created on Sat May  5 23:40:17 2018

@author: Laine Rumreich

Program to read in a poorly translated text file of SDP code and fix it to adhere to 
standards of coding.

"""

# Python imports
import re

# Local imports
from peek import peek
from stringIsBlank import isBlank

# Define lists of keywords
endChars = [';', '}', "{", '/']
lineBreaks = [';', '}', "{"]
endComments = ["#", "void ", "int ", "bool ", "float ", "double ", "char ", "class ", "LCD.", "::", ';', '}', ':', '{', "//"]
commentKeywords = ["while (", "while(", "for",  "if (", "if(", "else", "switch (", "switch("]
noEndChar = False

# Handle for loops that are broken up
def fixForLoop (line, dataFile, outputFile):
    fixedLine = "" # Reconstruct any broken for loops
    while(')' not in line):
        fixedLine = fixedLine + line.strip() + " "
        line = dataFile.readline()
       
    fixedLine = fixedLine + line.strip() + "\n"
    outputFile.write(fixedLine)   
  
# Return the full, syntactically correct preprocessor directive starting on this line
def analyzePreDir(line, dataFile):
    # Remove junk proceeding directive
    location = line.find("#")
    line = line[location:]
    
    preDirectiveLine = ""
    peekLine = peek(dataFile)
    directives = line.strip().split("#")

    for directive in directives:
        directive = directive.strip()
        if "include" in directive:
            if "include " not in directive:
                directive = directive.replace("include<", "include <") 
                
            # Make sure the current directive on this line has content
            splitLine = directive.split(" ");
            if len(splitLine) <= 1 and not isBlank(peekLine):
                nextLineDirectives = peekLine.split("#")
                directive = directive + " " + nextLineDirectives[0]

            preDirectiveLine += "#" + directive + "\n"  
        elif "define" in directive:
            # Make sure the define line has a correct space
            if "define " not in directive:
                directive = directive.replace("define", "define ")
                
            # Make sure the current directive on this line has content
            splitLine = directive.split(" ");
            if len(splitLine) <= 1 and not isBlank(peekLine):
                nextLineDirectives = peekLine.split("#")
                directive = directive + " " + nextLineDirectives[0]
                                                    
            preDirectiveLine += "#" + directive + "\n" 
    return preDirectiveLine           

# Print the fully combined comment starting on the current line
# (combine comments that span multiple lines)
def analyzeComment(line, dataFile, outputFile):
    
    # Keep combining lines into the comment until a keyword is found on the next line
    while True:
        
        peekLine = peek(dataFile) # Peek at the next line in the file
        
        # If any keywords in line, print comment and restart analyzeLine at that point
        if(any(ck in line for ck in commentKeywords) and not "print" in line):
            
            # Handle if the keyword is a for loop (special case)
            if("for" in line):
                # Get the location of "for"
                forLocation = line.find("for") + 2
            
                # Check that "(" comes directly after it
                if("(" in line):
                    parenLocation = line.find("(")
                    if(parenLocation is forLocation + 1 or parenLocation is forLocation + 2):
                        fixForLoop(line, dataFile, outputFile)
                elif("(" in peekLine):
                    parenLocation = peekLine.strip().find("(")
                    if(parenLocation is 0):
                        fixForLoop(line, dataFile, outputFile)
                else: # the "for" was not actually a loop 
                    # Otherwise, write out the current part of the comment and get any
                    # remaining part of the comment in the next loop if needed
                    outputFile.write(line.strip() + " ")
                        
            # Handle all other keywords    
            elif("{" in line or ("{" in peekLine and not any(ck in peekLine for ck in commentKeywords))):
                # Split the line into the comment and the comment keyword
                splitLine = re.search('while|if|else|switch', line, 1) # regular expression
                
                if splitLine is not None: # Make sure there was a keyword; should never fail
                    index = splitLine.start(0)
                    
                    # Print the comment
                    comment = line[:index]
                    outputFile.write(comment.strip() + "\n")
                    
                    # Analyze the line starting at the keyword and exit comment
                    analyzeLine(line[index:], dataFile, outputFile)
                    break
                        
        else:
            # Otherwise, write out the current part of the comment and get any
            # remaining part of the comment in the next loop if needed
            outputFile.write(line.strip() + " ")
        
        # Do while
        # Note: since "int" is a keyword, "print" tends to be found accidentally
        if isBlank(peekLine) or (any(endC in peekLine for endC in endComments) and not "print" in peekLine):
            break
        line = dataFile.readline() # only read the next line if it is part of the comment
        
    outputFile.write("\n")

# Parse a single data file and record the analyzed data in the variable count
def parseFile(dataFile, outputFile):
    line = dataFile.readline()
    while (line):
        analyzeLine(line, dataFile, outputFile)        
        line = dataFile.readline()

# Analyze a single line of the input file
def analyzeLine(line, dataFile, outputFile):
    global noEndChar
    location = 0
    ifEndComment = False
    endComment = ""
    
    line = line.lstrip()
    
    # Ignore blank lines
    if(isBlank(line)):
        return
    
    ###########################################################################
    #          Handle Comment and Preprocessor Directive Lines                #
    ###########################################################################
    
    # Handle lines that are only a comment
    if(len(line) >= 2 and line[0] is "/" and line[1] is "/"):
        analyzeComment(line, dataFile, outputFile)
        return
        
    # Handle comments that come at the end of other lines of code
    elif("//" in line):
        ifEndComment = True
        location = line.find("//")
        endComment = line[location:]
        line = line[:location] # Remove comment from line to print later
    
    # If this is a preprocessor directive line, fix up the line and print it
    if("#include" in line or "#define" in line):
       preDirective = analyzePreDir(line, dataFile) 
       outputFile.write(preDirective)
       
       # Print out any comment that goes at the end of a line
       if(ifEndComment):
            analyzeComment(endComment, dataFile, outputFile)
            
       return
           
    ###########################################################################
    #                  Handle Various Single-Line Issues                     #
    ###########################################################################
    
    # Fix type keywords not separated by a space
    if "int " not in line:
        line = line.replace("int", "int ")
    if "long " not in line:
        line = line.replace("long", "long ")
    if "void " not in line:
        line = line.replace("void", "void ")
    if "bool " not in line:
        line = line.replace("bool", "bool ")
    if "float " not in line:
        line = line.replace("float", "float ")
    if "double " not in line:
        line = line.replace("double", "double ")
    if "char " not in line:
        line = line.replace("char", "char ")
        
    # Handle broken for loops not in comments
    peekLine = peek(dataFile)
    if(len(line) > 2 and line[:3] == "for"):
        # Get the location of "for"
        forLocation = line.find("for") + 2
        
        # Check that "(" comes directly after it
        if("(" in line):
            parenLocation = line.find("(")
            if(parenLocation is forLocation + 1 or parenLocation is forLocation + 2):
                fixForLoop(line, dataFile, outputFile)
        elif("(" in peekLine):
            parenLocation = peekLine.strip().find("(")
            if(parenLocation is 0):
                fixForLoop(line, dataFile, outputFile)
        
        return
    
    ###########################################################################
    #                       Print Non-Comment Line                            #
    ###########################################################################
       
    # If there is a comment at the end of the line, the line of code is complete
    # so print out the line and then the comment
    if(ifEndComment):
        outputFile.write(line.strip() + " ")
        analyzeComment(endComment, dataFile, outputFile)
        return
            
    # Combine lines separated by a newline that should not be
    if(not any(ec in line for ec in endChars)):
        outputFile.write(line.strip() + " ")
        noEndChar = True
    else: # Separate lines that have multiple end characters or print full lines  
        noEndChar = False
        while("{" in line or "}" in line or ";" in line):
            
            # Get the index of the first line break character in line
            index = next((i for i, ch in enumerate(line) if ch in lineBreaks), None)
                      
            outputFile.write(line[:index+1].strip() + "\n")
            
            line = line[index+1:]
        
        # Handle broken for loops combined with other lines
        peekLine = peek(dataFile)
        if(len(line) > 2 and line[:3] == "for"):
            # Get the location of "for"
            forLocation = line.find("for") + 2

            # Check that "(" comes directly after it
            if("(" in line):
                parenLocation = line.find("(")
                if(parenLocation is forLocation + 1 or parenLocation is forLocation + 2):
                    fixForLoop(line, dataFile, outputFile)
            elif("(" in peekLine):
                parenLocation = peekLine.strip().find("(")
                if(parenLocation is 0):
                    fixForLoop(line, dataFile, outputFile)
            return
                        
        # Combine lines now separated by a newline that should not be
        # From anything remaining on the end of the current line
        if(not isBlank(line)):
            outputFile.write(line.strip() + " ")
            noEndChar = True
            
       
def cleanFile(dataFile, fileName):  
    # Create an edited version of the file to be deleted later
    outputName = fileName[:5] + "edited" + fileName[5:]
    outputFile = open(outputName, "w")
    
    parseFile(dataFile, outputFile)
    outputFile.write("\n") # make sure file ends in a newline
    dataFile.close()    
