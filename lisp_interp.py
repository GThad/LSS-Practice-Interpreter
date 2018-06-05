import io
from lss_lexer.lss_lexer import lex
from lss_parser.lss_parser import parse
from lss_analyzer.lss_analyzer import analyze

progIO = io.StringIO()
#progIO.write("(+ (* 9 (+ 2.56 3)) (- 10 5)) \n"
#             +"(append 4 \"as \\n dqwqe\")")
progIO.write("(+ (+ 2 3) 4)")aqw
progIO.seek(0)

tokens, lexErrors = lex(progIO)
ast, parseErrors = parse(tokens)
namespace, semantErrors = analyze(ast)

print(namespace.env)
print(namespace.query("+"))
for error in semantErrors:
    print(error)


