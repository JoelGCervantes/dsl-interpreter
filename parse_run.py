from interp import (
    Expr, eval, Lit, Name, Let, If, Letfun, App,
    Add, Mul, Sub, Eq, Not, And, Or, Concat, Replace
)
from lark import Lark, Token, ParseTree, Transformer
from lark.exceptions import VisitError
from pathlib import Path

parser = Lark(Path('expr.lark').read_text(), start='expr', parser= 'earley', ambiguity='explicit')

class ParseError(Exception):
    pass

def parse(s: str) -> ParseTree:
    try:
        return parser.parse(s)
    except Exception as e:
        raise ParseError(e)

class AmbiguousParse(Exception):
    pass

class ToExpr(Transformer[Token, Expr]):
    def let(self, args: tuple[Token, Expr, Expr]) -> Expr:
        return Let(args[0].value, args[1], args[2])
    
    def id(self, args: tuple[Token]) -> Expr:
        return Name(args[0].value)
    
    def int(self, args: tuple[Token]) -> Expr:
        return Lit(int(args[0].value))
    
    def bool(self, args: tuple[Token]) -> Expr:
        return Lit(args[0].value == 'true')
    
    def str(self, args: tuple[Token]) -> Expr:
        return Lit(args[0].value[1:-1])  # remove surrounding quotes
    
    def if_(self, args: tuple[Expr, Expr, Expr]) -> Expr:
        return If(args[0], args[1], args[2])
    
    # Function definition (letfun): name, param, bodyexpr, inexpr
    def letfun(self, args: tuple[Token, Token, Expr, Expr]) -> Expr:
        # args: [name Token, param Token, bodyexpr Expr, inexpr Expr]
        return Letfun(args[0].value, args[1].value, args[2], args[3])
    
    # Function application (app)
    def app(self, args: tuple[Expr, Expr]) -> Expr:
        return App(args[0], args[1])
    
    def plus(self, args: tuple[Expr, Expr]) -> Expr:
        return Add(args[0], args[1])
    
    def times(self, args: tuple[Expr, Expr]) -> Expr:
        return Mul(args[0], args[1])
    
    def minus(self, args: tuple[Expr, Expr]) -> Expr:
        return Sub(args[0], args[1])
    
    def eq(self, args: tuple[Expr, Expr]) -> Expr:
        return Eq(args[0], args[1])
    
    def not_(self, args: tuple[Expr]) -> Expr:
        return Not(args[0])
    
    def and_(self, args: tuple[Expr, Expr]) -> Expr:
        return And(args[0], args[1])
    
    def or_(self, args: tuple[Expr, Expr]) -> Expr:
        return Or(args[0], args[1])
    
    def concat(self, args: tuple[Expr, Expr]) -> Expr:
        return Concat(args[0], args[1])
    
    def replace(self, args: tuple[Expr, Expr, Expr]) -> Expr:
        return Replace(args[0], args[1], args[2])
    
    def _ambig(self, _) -> Expr:
        raise AmbiguousParse()

def genAST(t: ParseTree) -> Expr:
    try:
        return ToExpr().transform(t)
    except VisitError as e:
        if isinstance(e.orig_exc, AmbiguousParse):
            raise AmbiguousParse()
        else:
            raise e

def just_parse(s: str) -> (Expr | None):
    '''Parses and pretty-prints an expression'''
    try:
        t = parse(s)
        print("raw:", t)
        print("pretty:")
        print(t.pretty())
        ast = genAST(t)
        print("raw AST:", repr(ast))  # use repr() to avoid str() pretty-printing
        return ast
    except AmbiguousParse:
        print("ambiguous parse")
    except ParseError as e:
        print("parse error:")
        print(e)
    return None

def parse_and_run(s: str):
    t = parse(s)
    ast = genAST(t)
    result = eval(ast)
    print(f"Input: {s}")
    print(f"Result: {result}")

# ---------------------------------------
# Test expressions showing domain-specific syntax
# ---------------------------------------

if __name__ == "__main__":
    parse_and_run('"Hello, " ++ "world!"')  # String concatenation

    parse_and_run('replace("the hat", "hat", "cat")')  # Replace 'hat' with 'cat'

    parse_and_run('let s = "a big dog" in replace(s, "big", "small")')  # Let + replace

    parse_and_run('let greeting = "Hi" in greeting ^ ", there!"')  # Let + concat

    parse_and_run('replace("blue sky", "blue", "red") ^ " sunset"')  # Replace + concat

    parse_and_run('if true then replace("hot", "hot", "cold") else "no change"')  # If + replace

    parse_and_run('if false then "won\'t show" else "show this" ^ " now"')  # If + concat
