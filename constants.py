# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 17:31:35 2018

@author: Laine Rumreich

Constants used primarily in analyzeLine.py.
"""

END_CHARS = [';', '}', '{']
COMMENTS = ["//", "/*"]
END_COMMENTS = [';', '}', '{', ")", "#", "=", "//"]
TIME_FUNCTIONS = ["TimeNow", "Sleep("]
RAND_FUNCTIONS = ["rand(", "Rand("]
PLOT_FUNCTIONS = ["plot("]
PRINT_KEYWORDS = ["LCD.", "printf(", "scanf("]
NOT_PRINT_KEYWORDS = ["#"]
WRITE_KEYWORDS = [".Write", ".Set"]
WHILE_KEYWORDS = ["while (", "while("]
DO_KEYWORDS = ["do{", "do {", "do\n"]
FOR_KEYWORDS = ["for (", "for("]
IF_KEYWORDS = ["if (", "if("]
SWITCH_KEYWORDS = ["switch (", "switch("]
INPUT_KEYWORDS = ["input(", ".Touch"]
FUNCTION_KEYWORDS = ["void", "int", "bool", "float", "double", "char", "long", "::"]
TYPE_KEYWORDS = ["void", "int", "bool", "float", "double", "char", "long"]
NOT_FUNCTION_KEYWORDS = ["main", "for(", "for (", "while(", "while ", "if(", "if (", "LCD", "class", ";"]

# Halstead Complexity Operators (order matters)
STOR_SPEC = ["auto", "extern", "register", "static", "typedef"]
TYPE_QUAL = ["const", "final", "volatile"]
RESERVED = ["break", "case:", "case :", "continue", "default", "do", "if(", "if (", "else", "enum", "for(", "for (", "goto", "new", "return", "sizeof", "struct", "switch", "union", "while(", "while ("]
OPERATOR = ["!=", "!", "%=", "%", "&&", "&=", "&", "=&", "||", "(", "{", "[", "*=", "*", "++", "+=", "+", ",", "--", "-=", "->", "-", "...", ".", "/=", '/', "\\", "::", ":", "<<", "<<=", "<=", "<", "==", "=", ">=", ">>", ">>=", ">", "?", "^^=", "|=", "|", "~", ";", "“", '"', "‘", "'", "##", "#"]
OPERATORS = STOR_SPEC + TYPE_QUAL + RESERVED
PRE_DIRECTIVES = ["#define", "#include"]