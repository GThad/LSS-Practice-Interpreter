This repository contains the files for an interpreter (built in Python)
for a modified subset of LISP. This language was built for practice in
compiler writing. The language itself is simple but non-trivial. It
supports the following:

    . Boolean logic
    . Integer and floating point arithmetic
    . Strings and string manipulation
    . List manipulation
    . Single line comments
    . First class functions and lambdas
    . Multiple return values
    . Identifier shadowing
    . Contract based design: preconditions and postconditions
    . Probably more
    
The syntax for the language is given by the following (somewhat informal) grammar.
Note that the word "empty" refers to the empty string, and that newlines
should be ignored. The word "anychar" is used to refer to any UTF-8
character. The word "digit" is used to refer to any digit 0 through 9.
The "+" and "*" notations are used as with regular expressions.
-------------------------------------------------------------------------------
Program <- [Expr]*
          
Expr <- "(" "def" Symbol Atom ")"
      | "(" "defun" Symbol "(" [Symbol]* ")" RequireExpr 
        [SubExpr]+ EnsureExpr ")"
      | SubExpr

RequireExpr <- "(" "require" SubExpr ")"

EnsureExpr <- "(" "ensure" SubExpr ")"

SubExpr <- "(" Symbol ")"
         | "(" Symbol [SubExpr]* ")
         | Atom

Atom <- Number
      | String
      | Symbol
      
Number <- Integer
        | Float
        
String <- "\"" [anychar]* "\""
    
Integer <- [digit]+
         | "-" [digit]+
            
Float <- [digit]* "." [digit]+
       | [digit]+ "." [digit]*
       | "-" [digit]* "." [digit]+
       | "-" [digit]+ "." [digit]*

Symbol is anything else.

Comments are given by ";" and extend to the end of the line.
-------------------------------------------------------------------------------

Some miscellaneous details:

    . No Atom can be written over multiple lines. If one wants
      to construct such large atoms, then use built in functions.
    . Newlines in Strings must be given explicitly with "\n".
    . No Atom can have whitespace other than strings.
    . Due to the definitions of Symbols being "anything else",
      we can get odd but valid names like "!@+..04".
    . Symbols cannot contain parentheses, but can contain other brackets.
    . The character "-" for negative numbers must not be followed by whitespace.
    