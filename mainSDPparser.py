# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 13:18:13 2018

@author: Laine Rumreich

Program to read in a text file wih FEH SDP code and analyze it for coding 
techniques, complexity, and good and bad coding practices. Then, print 
the results to an excel spreadsheet.
"""  

# Python imports
import os
from openpyxl import Workbook

# Local imports
from printOutput import printOutput
from parseFile import parseFile
from writeHeader import writeHeader
from cleanFile import cleanFile   

def main():
    
    # Define excel spreadsheet variables
    lineNum = 2 # The line the current output should be written on
    lineString = "A"
    
    # Ask the user for a text input file that contains all the filenames for the 
    # SDP text files to analyze
    nameList = input("Enter a file with the names of the files to analyze: ")
    
    # Open the .txt data file containing list of filenames
    if(not os.path.isfile(nameList)):
        print("No such file or directory: '" + nameList + "'")
        return
    nameFile = open(nameList, 'r')    
    name = nameFile.readline()
    
    # Open an excel spreadsheet to print the output
    wb = Workbook() # Open the output file
    output = wb.active # Get the active worksheet
    writeHeader(output) # Write the header to the output file
    
    # Read in each file name in the nameFile, and run the program on it
    while(name):
        # Open the current file
        fileName = name[:-1] # Consume newline character
        fileName = "Data" + '\\' + fileName + ".txt"
        if(not os.path.isfile(fileName)):
            print(fileName, " is not a valid file.")
            name = nameFile.readline()
            continue
        dataFile = open(fileName, 'r')
        
        # Compute which line the current output should go on
        lineString = lineString[0]
        lineString = lineString + str(lineNum)
        
        # Print the name of the current file
        output[lineString] = name
        
        # Clean up the current file for easier analysis
        cleanFile(dataFile, fileName)
        dataFile.close()
        
        # Access the edited data file created in cleanFile, to be deleted later
        editedDataFileName = fileName[:5] + "edited" + fileName[5:]
        editedDataFile = open(editedDataFileName, 'r')
        
        counts = {'lines': 0,
                  'comments': 0,
                  'forLoops': 0,
                  'whileLoops': 0,
                  'nestedLoops': 0,
                  'highestNestedLoop': 0, #TODO
                  'ifElse': 0,
                  'nestedIfs': 0,
                  'time': 0,
                  'rand': 0,
                  'input': 0,
                  'plot': 0,
                  'print': 0,
                  'switch': 0,
                  'cyclomatic': 0,
                  'cyclAvg': 0,
                  'cyclMed': 0,
                  'halsteadVolume': 0,
                  'halsteadDifficulty': 0,
                  'halsteadEffort': 0,
                  'maintainability': 0,
                  'userFunc': 0,
                  'addFunc': 0} #TODO
        
        # Read in the data from the input file and perform the primary analysis
        parseFile(editedDataFileName, editedDataFile, counts)
        
        # Print the results of the analysis to the output excel file
        printOutput(output, lineNum, counts)
        print("Finished reading in file: ", fileName)
        lineNum += 1
        
        # Close the current (edited) input data file
        editedDataFile.close()
        
        # Remove the edited file
        os.remove(editedDataFileName)
        
        # Read in the next name from the nameFile
        name = nameFile.readline()
        
    # Close the user-entered file of program names   
    nameFile.close()
    
    # Save the output file
    wb.save("output.xlsx")
    
if __name__ == "__main__":
    main()
    print("Done with program. Exiting...")
