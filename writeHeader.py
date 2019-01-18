# -*- coding: utf-8 -*-
"""
Created on Sun May 20 16:45:06 2018

@author: Laine Rumreich

Write the header to the output data file.
"""

def writeHeader(output):
    output['B1'] = "Number of Lines of code (do not include comments)"
    output['C1'] = "Number of lines of comments, if a block of comments, count as 1"
    output['D1'] = "For Loops"
    output['E1'] = "While Loops"
    output['F1'] = "Nested Loops"
    output['G1'] = "Highest Level of Nested Loop"
    output['H1'] = "If/Else statements"
    output['I1'] = "Embedded If Statements"
    output['J1'] = "Time Functions"
    output['K1'] = "Random Numbers"
    output['L1'] = "Input Statements"
    output['M1'] = "Plotting"
    output['N1'] = "Print Statements"
    output['O1'] = "Switch Cases"
    output['P1'] = "Cyclomatic Complexity"
    output['Q1'] = "Mean Block Cyclomatic Complexity"
    output['R1'] = "Median Block Cyclomatic Complexity"
    output['S1'] = "Halstead Volume"
    output['T1'] = "Halstead Difficulty"
    output['U1'] = "Halstead Effort"
    output['V1'] = "Maintainability Index"
    output['W1'] = "User Defined Functions"
    output['X1'] = "Additional Functions"
    output['Y1'] = "Bad Programming Practices"