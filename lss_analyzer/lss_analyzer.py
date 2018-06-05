from typing import List, Dict, NewType, TypeVar
from lss_lexer.lss_token import Token, TokenType
from lss_env.namespace import NameSpace
from lss_env.comp_obj import CompObj, DummyCompObj, globalEnv

# Type Aliases
Symbol = NewType("Symbol", str)
String = NewType("String", str)
Number = TypeVar("Number", int, float)
Boolean = NewType("Boolean", bool)
Atom = TypeVar("Atom", Symbol, String, Number, Boolean)
Expr = TypeVar("Expr", Atom, List["Expr"])
Env = NewType("Env", Dict[str, CompObj])

def analyze(ast):
    """
    Should produce an namespace object and a list of errors.
    These two return objects are defined as empty here and are
    mutated in the helper function, which works recursively.
    """
    namespace = NameSpace("global", globalEnv, [], None)
    errors = []
    for expr in ast:
        semant(expr, namespace, errors)
    return (namespace, errors)

def semant(expr, namespace, errors):
    # Handle case when the expression is only an atom
    if isinstance(expr, Token):
        if expr.isSym():
            compObj = namespace.query(expr[1]) 
            if (not compObj):
                errors.append(SyntaxError(
                    "SemanticError: Undefined symbol: \n"
                    + "\t {} \n".format(expr[1])
                    + "seen on line {} column {}".format(expr[3], expr[4])))
                return DummyCompObj()
            else:
                return compObj
        else:
            return CompObj(expr[1], lambda: None)
    # Handle case when expression is a list of expression
    else:
        compObjs = [semant(subExpr, namespace, errors)
                    for subExpr in expr]
        calleeCompObj = compObjs[0]
        if (not calleeCompObj.isFunc()):
            errors.append(SyntaxError(
                "SemanticError: Symbol: \n"
                + "\t {} \n".format(expr[0][1])
                + "on line {} column {} must refer to a function".format(
                        expr[0][3], expr[0][4])))
            return DummyCompObj()
        else:
            return calleeCompObj.semant(namespace, errors, compObjs[1:])