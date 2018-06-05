from typing import List, Dict, NewType, TypeVar
from lss_lexer.lss_token import Token, TokenType

# Type Aliases
Symbol = NewType("Symbol", str)
String = NewType("String", str)
Number = TypeVar("Number", int, float)
Boolean = NewType("Boolean", bool)
Atom = TypeVar("Atom", Symbol, String, Number, Boolean)
Expr = TypeVar("Expr", Atom, List["Expr"])

class CompObj():
    
    def __init__(self, value, semantFunc):
        self.value = value
        self.semant = semantFunc
        
    def isFunc(self):
        return False

class FuncObj(CompObj):
    
    def __init__(self, value, name, numArgs, semantFunc):
        super().__init__(value, semantFunc)
        self.name = name
        self.numArgs = numArgs

    def isFunc(self):
        return True
    
class DummyCompObj(CompObj):
    
    def __init__(self):
        super().__init__(None, lambda x, y, z: self)
        
    def isFunc(self):
        return True

Env = NewType("Env", Dict[str, CompObj])

plusCompObj = FuncObj((lambda x, y: x + y), 
                      "+", 2, 
                      (lambda namespace, errors, argsCodeObjs: 
                          DummyCompObj()))

globalEnv = {
    "+": plusCompObj    
    }

