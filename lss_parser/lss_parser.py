from typing import List, Tuple, NewType, TypeVar
from lss_lexer.lss_token import Token, TokenType

# Type Aliases
Symbol = NewType("Symbol", str)
String = NewType("String", str)
Number = TypeVar("Number", int, float)
Boolean = NewType("Boolean", bool)
Atom = TypeVar("Atom", Symbol, String, Number, Boolean)
Expr = TypeVar("Expr", Atom, List["Expr"])

def parse(tokens: List[Token]) -> Tuple[List[Expr], List[SyntaxError]]:
    """
    Parses the output of the lexer into an AST and provides a list of 
    errors.
    
    Args:
        tokens (List[Token]): The list of tokens to parse. This should
            be output from lisp_lexer.lex
        
    Returns:
        A tuple (ast, errors) where ast is a list of expression
        representing the abstract syntax tree, and errors is a list of
        syntax errors that were found during the parsing phase.
    """
    # Reverse tokens since the tokens list is used as a stack.
    # Appending and removing from end of list in Python is faster.
    tokens.reverse()
    nodes = []
    errors = []
    
    # parse_helper only parses one complete expression. We do
    # repeated calls to handle more than one complete expression
    # such as "(+ 1 2) (- 2 1)"
    while len(tokens) != 0:
        innerNodes, innerErrors = _parse_helper(tokens)
        if innerNodes != []:
            nodes.append(innerNodes)
        if innerErrors != []:
            errors.extend(innerErrors)
    
    return (nodes, errors)

def _parse_helper(tokens: List[Token]):
    """ 
    Parses a single complete expression that lies on the stack
    given by tokens. Note that this function realies
    on the fact that the token list is mutable.
    """
    errors = []
    node = []

    # If there are no more tokens, then there is nothing
    # to parse
    if (not tokens):
        return ([], [])

    token = tokens.pop()
    
    if token[2] == TokenType.RPAREN:
        # See ), then there is no matching ( before
        errors.append(SyntaxError("SyntaxError: Unmatched \")\""
                      + " at line {} column {}".format(token[3], token[4])))
        # Attempt to parse the rest of the tokens    
        innerNode, innerErrors = _parse_helper(tokens)
        node = innerNode
        errors.extend(innerErrors)
        return (node, errors)
    elif token[2] == TokenType.LPAREN:
        # See (, then keep parsing until we see the matching )
        while tokens and tokens[-1][2] != TokenType.RPAREN:
            innerNodes, innerErrors = _parse_helper(tokens)
            node.append(innerNodes)
            errors.extend(innerErrors)
        # Pop off the matching ) if it exists
        if  tokens:
            tokens.pop()
        else:
            errors.append(SyntaxError(
                    "SyntaxError: Missing one or more \")\""))
        return (node, errors)
    else:
        # Otherwise, we have an atom, return its token.
        return (token, errors)
    
    return (node, errors)
    
