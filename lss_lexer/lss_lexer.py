from typing import List, Tuple, TextIO, NewType, TypeVar
from lss_lexer.lss_token import Token, TokenType

# Type Aliases
Symbol = NewType("Symbol", str)
String = NewType("String", str)
Number = TypeVar("Number", int, float)
Boolean = NewType("Boolean", bool)
Atom = TypeVar("Atom", Symbol, String, Number, Boolean)

def lex(stream: TextIO) -> List[Token]:
    """ 
    Lexes a text character stream into a list of tokens.
    
    Args:
        stream (io.TextIOBase): The text stream to read from.
        
    Returns:
        A tuple (tokes, errors) where tokens is a list of tokens
        representing the tokenized program, and errors is a list of
        syntax errors that were found during the lexing phase.
    """
    tokens = []
    errors = []
    
    codeDump = _dump_stream(stream)
    
    # In case of empty program, there are no tokens or errors
    if (not codeDump):
        return ([],[])
    
    # The end of the program is padded with a newline, which
    # acts as a terminator for the programs
    lastChar = codeDump[len(codeDump) - 1]
    codeDump.append(("\n", lastChar[1], lastChar[2] + 1))
    
    currTokenStr = ""
    inAtom = False
    inStrAtom = False
    
    # Lexing is essentially done by a state machine, reading
    # character by character, that
    # adds tokens and errors as side effects. The transition details
    # of the state machine are given by the if-elif-else chains.
    # The state is described by currTokenStr, inAtom, and inStrAtom.
    for char, lineNum, colNum in codeDump:
        if (not inAtom):
            if char == "(":
                # Seen (, add its token
                tokens.append(Token("(", "(", TokenType.LPAREN,
                                           lineNum, colNum))
            elif char == ")":
                # Seen ), add its token
                tokens.append(Token(")", ")", TokenType.RPAREN,
                                           lineNum, colNum))
            elif char.isspace():
                # Ignore whitespace
                pass
            elif char == "\"":
                # See quote, starting string atom
                inAtom = True
                inStrAtom = True
            else:
                # Anything else, starting non-string atom
                currTokenStr = currTokenStr + char
                inAtom = True
        elif inStrAtom:
            if char == "\"":
                # See closing quote, ending string atom
                tokens.append(Token("\"" + currTokenStr + "\"", 
                              _fix_escapes(currTokenStr), 
                              TokenType.STR, lineNum,
                              colNum))
                currTokenStr = ""
                inAtom = False
                inStrAtom = False
            elif char == "\n":
                # See newline, problem: newline much occur after closing
                # quote
                errors.append(SyntaxError(
                    "Syntax Error: Expected closing quotation mark after \n"
                    + "\t {} \n".format("\"" + currTokenStr + "\"")
                    + "on line {} and column {}".format(lineNum, colNum)))
                currTokenStr = ""
                inAtom = False
                inStrAtom = False
            else:
                # Anything else, character is part of string
                currTokenStr = currTokenStr + char
        else:
            if char.isspace():
                # See whitespace, finished atom with whitespace
                tokens.append(_tokenize_atom(currTokenStr, lineNum,
                                              colNum-1))
                currTokenStr = ""
                inAtom = False
            elif char == "(":
                # See (, finished atom with (
                tokens.append(Token("(", "(", TokenType.LPAREN,
                                           lineNum, colNum))
                tokens.append(_tokenize_atom(currTokenStr, lineNum,
                                              colNum-1))
                currTokenStr = ""
                inAtom = False
            elif char == ")":
                # See ), finished atom with )
                tokens.append(_tokenize_atom(currTokenStr, lineNum,
                                              colNum-1))
                tokens.append(Token(")", ")", TokenType.RPAREN,
                                           lineNum, colNum))
                currTokenStr = ""
                inAtom = False
            else:
                # Anything else, char is part of atom
                currTokenStr = currTokenStr + char
    return (tokens,errors)

def _tokenize_atom(tokenStr:str, lineNum:int, colNum:int) -> Token:
    """
    Given a string of code representing a token, return
    the corresponding Token object.
    """
    if _isBool(tokenStr):
        boolValue = True if tokenStr == "true" else False
        return Token(tokenStr, boolValue, TokenType.BOOL, 
                     lineNum, colNum)
    elif _isInt(tokenStr):
        return Token(tokenStr, int(tokenStr), TokenType.INT, 
                     lineNum, colNum)
    elif _isFloat(tokenStr):
        return Token(tokenStr, float(tokenStr), TokenType.FLOAT, 
                     lineNum, colNum)
    else:
        return Token(tokenStr, tokenStr, TokenType.SYM, 
                     lineNum, colNum)
        
def _isBool(tokenStr:str) -> bool:
    return tokenStr == "true" or tokenStr == "false"

def _isInt(tokenStr:str) -> bool:
    if tokenStr[0] == "-":
        return tokenStr[1:].isnumeric()
    else:
        return tokenStr.isnumeric()
    
def _isFloat(tokenStr:str) -> bool:
    if tokenStr[0] == "-":
        if tokenStr[1:].count(".") == 1:
            return tokenStr[1:].replace(".", "").isnumeric()
        else:
            return False
    else:
        if tokenStr.count(".") == 1:
            return tokenStr.replace(".", "").isnumeric()
        else:
            return False
        
def _fix_escapes(astr:str) -> str:
    """
    Given a string with escaped characters written out literally,
    this return the same string with the literal escapes converted
    into escaped characters.
    """
    return bytes(astr, "utf-8").decode("unicode_escape")

def _dump_stream(stream: TextIO) -> List[Tuple[str, int, int]]:
    """
    Gets every character from a text stream and dumps it into a list
    of tuples (char, lineNum, colNum) holding the characters and
    location metadata.
    """
    dump = []
    lines = stream.readlines()
    for lineNum, line in enumerate(lines):
        for colNum, char in enumerate(line):
            dump.append((char, lineNum+1, colNum+1))
    return dump