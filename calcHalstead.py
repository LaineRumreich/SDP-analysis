# -*- coding: utf-8 -*-
"""
Created on Sat Jul  7 21:37:15 2018

@author: Laine Rumreich

Halstead´s metrics is based on interpreting the source code as a sequence of 
tokens and classifying each token to be an operator or an operand.

Then the operators and operands are recorded using the following variables
    n1: number of unique (distinct) operators
    n2: number of unique (distinct) operands
    N1: total number of operators
    N2: total number of operands
    m: number of modules (functions)

The Halstead metrics are then computed according to the following formulas    
    Program length (N):      N = N1 + N2
    Program vocabulary (n):  n = n1 + n2
    *Volume (V):             V = N * LOG2(n)
    *Difficulty (D):         D = (n1/2) * (N2/n2)
    *Effort (E):             E = D * V
    Average Volume (avgV)    avgV = sum(V)/m
    Average Effort (avgE)    avgE = sum(E)/m

* denotes values recorded in data spreadsheet

The following section rigorously defines how operators and operands were 
identified and distinguished in this program. These definitions are necessary
because what defines an operand and operator tends to be open to interpretation.

    Operator:
        - type specifiers or qualifiers (static, typedef, const)
        - reserved words (asm, break, case, class, continue, default, delete, 
                          do, else, enum, for, goto, if, new, operator, private, 
                          protected, public, return, sizeof, struct, switch, 
                          this, union, while, namespace, using, try, catch, 
                          throw, const_cast, static_cast, dynamic_cast, 
                          reinterpret_cast, typeid, template, explicit, true, 
                          false, typename)
        - operators (!   !=   %   %=   &   &&   ||   &=   ( )   *   *=   +   ++
                     +=   ,   -   --   -=   ->   .   ...   /   /=   :   ::   < 
                     <<   <<=   <=   =   ==   >   >=   >>   >>=   ?   [ ]   ^  
                     ^=   {   }   |   |=   ~  ;)
        - control structures (for (...)   if (...)   switch (...)   while (...)  catch (...))
         
    Operand:
        - not operators
        - not whitespace
        - not comments
        
        - keywords
        - all identifiers that are not reserved words (user-defined variables)
        - constants (character, numeric, string, etc.)
        - type specifiers (bool, char, double, float, int, long, short, signed, unsigned, void)
        
        
    Some special cases are as follows :
        • A pair of parenthesis is considered a single operator.
        • The ternary operator ‘?’ followed by ‘:’ is considered a single operator as it is equivalent to “if-else”construct. 
        • A label is considered an operator if it is used as the target of a GOTO statement.
        • In the following control structures
            case ...: for (...), if (...), switch (...), while(...)
            the colon or the parentheses are counted together as one operator with the control.
        • Comments are considered neither an operator nor an operand.
        • The function name is considered a single operator when it appears as calling a function; but when it appears in fucntion declarations/definitions it is not counted as an operator.
        • Similarly, identifiers( or variables) and constants are not considered as operands when 
        they appear in declaration, but are are considered operands when they appear with operators 
        in expressions. 
            func(a,b);                          a and b are considered operands and ‘,’ and‘;’ operators 
            int func(int a , int b) {…….…….}    func, a and b are not operands
            
            
    Analyzing Results:
        The volume of a file should be at least 100 and at most 8000. 


"""

# Python imports
import math

class halsteadValues:
    # Intitialize the complexity variables volume, difficulty, and effort
    def __init__(self):
        self.volume = 0
        self.difficulty = 0
        self.effort = 0        
    
    # Calculate volume, difficulty, and effort values based on the operators and operands
    def calcHalstead(self, operatorList, operandList):
        n1 = len(operatorList)
        n2 = len(operandList)
        N1 = sum(operatorList.values())
        N2 = sum(operandList.values())
        n = n1 + n2
        N = N1 + N2     
        
        if n != 0:
            self.volume = N * math.log(n, 2)
        
        if n2 != 0:
            self.difficulty = n1/2 * N2/n2
            
        self.effort = self.difficulty * self.volume
    
    def getVolume(self):
        return self.volume
    
    def getDifficulty(self):
        return self.difficulty
    
    def getEffort(self):
        return self.effort
    