from lark import Lark, Transformer, v_args
from pathlib import Path
from interp import *  # Import all AST classes and eval functions

# Load the grammar
parser = Lark(Path('expr.lark').read_text(), start='expr', parser='earley', ambiguity='explicit')

# AST Transformer
class ToAST(Transformer):
    def int(self, items): return Lit(int(items[0]))
    def string(self, items): return Lit(Str(eval(items[0])))  # convert ESCAPED_STRING

    def id(self, items):
        name = str(items[0])
        if name == "true":
            return Lit(True)
        elif name == "false":
            return Lit(False)
        else:
            return Name(name)

    def plus(self, items): return Add(items[0], items[1])
    def minus(self, items): return Sub(items[0], items[1])
    def times(self, items): return Mul(items[0], items[1])
    def divide(self, items): return Div(items[0], items[1])
    def neg(self, items): return Neg(items[0])

    def and_(self, items): return And(items[0], items[1])
    def or_(self, items): return Or(items[0], items[1])
    def not_(self, items): return Not(items[0])

    def eq(self, items): return Eq(items[0], items[1])
    def lt(self, items): return Lt(items[0], items[1])
    def if_(self, items): return If(items[0], items[1], items[2])

    def let(self, items): return Let(str(items[0]), items[1], items[2])
    def letfun(self, items): return LetFun(str(items[0]), str(items[1]), items[2], items[3])
    def app(self, items): return App(items[0], items[1])

    def concat(self, items): return Concat(items[0], items[1])
    def replace(self, items): return Replace(items[0], items[1], items[2])

# Parse and run
def parse(s: str) -> Expr:
    tree = parser.parse(s)
    return ToAST().transform(tree)

def run(s: str):
    e = parse(s)
    print(f"Input: {s}")
    print(f"AST: {e}")
    print(f"Result: {eval(e)}")
    print()

# Test expressions
if __name__ == "__main__":
    run("true")
    run("false")
    run("1 + 2 * 3")
    run("\"hello\" ++ \" world\"")
    run("replace(\"cool cats\", \"cool\", \"smart\")")
    run("let x = 5 in x + 1 end")
    run("if true then 1 else 0")
    run("letfun f(x) = x + 1 in f(4) end")
