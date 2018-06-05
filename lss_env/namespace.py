from typing import List, NewType, TypeVar
from lss_lexer.lss_token import Token, TokenType

# Type Aliases
Symbol = NewType("Symbol", str)
String = NewType("String", str)
Number = TypeVar("Number", int, float)
Boolean = NewType("Boolean", bool)
Atom = TypeVar("Atom", Symbol, String, Number, Boolean)
Expr = TypeVar("Expr", Atom, List["Expr"])

class NameSpace():
    """
    A namespace has the following attributes:
        0. Namespace header
        1. An environment
        2. List of children namespaces
        3. Backpointer to parent namespace
    """
    
    def __init__(self, header, env, children, parent):
        self.header = header
        self.env = env
        self.children = children
        self.parent = parent
        
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
        
    def query(self, sym):
        if sym in self.env:
            return self.env[sym]
        else:
            if self.parent:
                return self.parent.query(sym)
            else:
                return False
        