import astor
from hy.lex import tokenize
from hy.lex.exceptions import PrematureEndOfInput
from hy.compiler import hy_compile



def getAST(code):
    try:
        a = tokenize(code)
        b = hy_compile(a, "hdb")
        ret = astor.dump(b)
    except PrematureEndOfInput:
        ret = "missing a paren"
    return ret

def getPython(code):
    try:
        a = tokenize(code)
        b = hy_compile(a, "hdb")
        ret =  astor.codegen.to_source(b)
    except PrematureEndOfInput:
        ret = "missing a paren"
    return ret

def codegen(code):
    ast = getAST(code)
    code_ret = getPython(code)
    return ast, code_ret

