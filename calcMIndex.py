# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 21:12:57 2018

@author: Laine Rumreich

Calculate the Maitainability Index of the given program. Maintainability Index 
is a software metric which measures how maintainable (easy to support and 
change) the source code is. The result is an index value between 0 and 100 that 
represents the relative ease of maintaining the code. A high value means better 
maintainability. 
[green rating]: 20-100
[yellow rating]: 10-19.99
[red rating]: 0-9.99

Formula (Microsoft derivative):
MI = MAX(0,(171 - 5.2 * ln(Halstead Volume) - 0.23 * (Cyclomatic Complexity) 
    - 16.2 * ln(Lines of Code))*100 / 171)
"""

# python imports
from math import log

def calcMIndex(linesOfCode, halsteadVolume, cyclomatic):
    MI = 0
    if linesOfCode > 0 and halsteadVolume > 0:
        MI = (171 - 5.2*log(halsteadVolume) - .23*cyclomatic - 16.2*log(linesOfCode))*100/171
    return max(0, MI)
    