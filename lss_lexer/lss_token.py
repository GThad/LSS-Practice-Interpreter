from enum import Enum
from typing import NewType, TypeVar, NamedTuple

# Type Aliases
Symbol = NewType("Symbol", str)
String = NewType("String", str)
Number = TypeVar("Number", int, float)
Boolean = NewType("Boolean", bool)
Atom = TypeVar("Atom", Symbol, String, Number, Boolean)

class TokenType(Enum):
    """
    The TokenType enum class contains an enumeration for token
    types. The token types themselves are given by strings.
    
    Note that all tokens are actually atoms and there are 5
    atoms prescribed by the language definitions: boolean 
    constants, integer constants, float constants, string 
    constants, and symbols. In this implementation, we further
    treat keyword symbols as their own token types.
    
    Attributes:
        LPAREN: "("
        RPAREN: ")"
        INT: "int"
        FLOAT: "float"
        STR: "string"
        SYM: "sym"
    """
    
    LPAREN = "("
    RPAREN = ")"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STR = "string"
    SYM = "sym"
    
    def __str__(self):
        return self.name

class Token(NamedTuple):
    """
    The Token class represents a token object, which contains
    the code string generating the token along with some metadata.
    
    Attributes:
        tokenStr (str): The code string generating this token.
        tokenVal (Atom): The evaluated value of this token, providing
            a mapping between LISP constants and Python values. The
            value is a Python int, float, and str if the token has is an
            integer, float, and string respectively. Symbols are represented
            as str as well.
        tokenType (TokenType): The type of the token.
        lineNum (int): An integer representing the line number
            the token was found. Note that this begins from 1.
        colNum (int): An integer representing the column of the last
            character in this token.
    """
    tokenStr: str
    tokenVal: Atom
    tokenType: TokenType
    lineNum: int
    colNum: int
    
    def __str__(self):
        return "<{}, {}, {}, {}>".format(
                             self.tokenVal, self.tokenType, 
                             self.lineNum, self.colNum)
        
    def isSym(self) -> bool:
        return self[2] == TokenType.SYM