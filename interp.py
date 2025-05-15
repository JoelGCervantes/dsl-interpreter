'''
Joel Garcia-Cervantes 
CS358 Principles of Programming Languages
Spring 2025

This file contains AST node definitions for expressions, an eval method for interpreting
expressions to values, and a run method for showing values to the use. It is part of Milestone 1 for the
term project.

'''
from dataclasses import dataclass

type Value = int | bool | Str | Closure

@dataclass
class Str():
    value: str
    def __str__(self) -> str:
        return f"{self.value}"
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Str):
            return self.value == other.value
        return False


type Expr = Or | And | Not | Lit \
            | Add | Sub | Mul | Div | Neg \
            |  Let | Name \
            | Eq | Lt | If \
            | Concat | Replace \
            | LetFun | App


@dataclass
class Or():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        # returns a string representation of the expression
        return f"({self.left} or {self.right})"

@dataclass
class And():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} and {self.right})"

@dataclass
class Not():
    subexpr: Expr
    def __str__(self) -> str:
        return f"(not {self.subexpr})"
    
@dataclass
class Lit():
    value: Value
    def __str__(self) -> str: 
        return str(self.value)

@dataclass
class Add():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} + {self.right})"

@dataclass
class Sub():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} - {self.right})"

@dataclass
class Mul():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} * {self.right})"

@dataclass
class Div():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} / {self.right})"
    
@dataclass
class Neg():
    subexpr: Expr
    def __str__(self) -> str:
        return f"(- {self.subexpr})"
    
@dataclass
class Let():
    name: str
    defexpr: Expr
    bodyexpr: Expr
    def __str__(self) -> str:
        return f"(let {self.name} = {self.defexpr} in {self.bodyexpr})"
    
@dataclass
class Name():
    name:str
    def __str__(self) -> str:
        return self.name

@dataclass
class Eq(): # equality 
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} == {self.right})"

@dataclass # less than 
class Lt():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} < {self.right})"

@dataclass
class If(): # if expression 
    cond: Expr
    then_branch: Expr
    else_branch: Expr
    def __str__(self) -> str:
        return f"(if {self.cond} then {self.then_branch} else {self.else_branch})"


@dataclass
class Concat():
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} + {self.right})"

@dataclass
class Replace():
    target: Expr
    old: Expr
    new: Expr 
    def __str__(self): return f"replace({self.target}, {self.old}, {self.new})"

@dataclass
class LetFun():
    name: str
    param: str
    funbody: Expr
    letbody: Expr
    def __str__(self):
        return f"(letfun {self.name}({self.param}) = {self.funbody} in {self.letbody})"

@dataclass
class App():
    funexpr: Expr
    actualarg: Expr
    def __str__(self):
        return f"({self.funexpr} {self.actualarg})"

@dataclass
class Closure():
    param: str
    body: Expr
    env: Env[Value]


type Binding[V] = tuple[str,V]  # this tuple type is always a pair
type Env[V] = tuple[Binding[V], ...] # this tuple type has arbitrary length 

from typing import Any
emptyEnv : Env[Any] = ()  # the empty environment has no bindings



def extendEnv[V](name: str, value: V, env:Env[V]) -> Env[V]:
    '''Return a new environment that extends the input environment env with a new binding from name to value'''
    return ((name,value),) + env



def lookupEnv[V](name: str, env: Env[V]) -> (V | None) :
    '''Return the first value bound to name in the input environment env
       (or raise an exception if there is no such binding)'''
    # exercises2b.py shows a different implementation alternative
    match env:
        case ((n,v), *rest) :
            if n == name:
                return v
            else:
                return lookupEnv(name, rest) # type:ignore
        case _ :
            return None  
        
        

class EvalError(Exception):
    pass


def eval(e: Expr) -> Value:
    return evalInEnv(emptyEnv, e)

def evalInEnv(env: Env[Value], e:Expr) -> Value:
    match e:
        # boolean expression forms
        case Or(l,r):
            lv = evalInEnv(env,l)
            if type(lv) is not bool:
                raise EvalError(f"or operator requires a boolean operand, but got {l}")
            if lv:
                return True
            rv = evalInEnv(env,r)
            if type(rv) is not bool:
                raise EvalError(f"or operator requires a boolean operand, but got {r}")
            return rv
        case And(l,r):
            lv= evalInEnv(env,l)
            if type(lv) is not bool:
                raise EvalError(f"and operator requires a boolean operand, but got {l}")
            if not lv:
                return False

            rv = evalInEnv(env,r)
            if type(rv) is not bool:
                raise EvalError(f"and operator requires a boolean operand, but got {r}")
            return rv
        case Not(s):
            i = evalInEnv(env,s)
            if type(i) is not bool:
                raise EvalError(f"not operator requires a boolean operand, but got {s}")
            return not i
            '''
            sv = evalInEnv(env,s)
            if isinstance(sv, bool):
                return not sv
            else:
                raise EvalError(f"not operator requires a boolean operand, but got {s}")
            '''
            
        # arithmetic(int) expression forms
        case Add(l,r):
            lv = evalInEnv(env,l)
            rv = evalInEnv(env,r)
            if type(lv) is int and type(rv) is int:
                return lv + rv
            else:
                raise EvalError("addition of non-integers")
        case Sub(l,r):
            lv = evalInEnv(env,l)
            rv = evalInEnv(env,r)
            if type(lv) is int and type(rv) is int:
                return lv - rv
            else:
                raise EvalError("subtraction of non-integers")
        case Mul(l,r):
            lv = evalInEnv(env,l)
            rv = evalInEnv(env,r)
            if type(lv) is int and type(rv) is int:
                return lv * rv
            else:
                raise EvalError("multiplication of non-integers")
        case Div(l,r):
            lv = evalInEnv(env,l)
            rv = evalInEnv(env,r)
            if type(lv) is int and type(rv) is int:
                if rv == 0:
                    raise EvalError("division by zero")
                else:
                    return lv // rv
            else:
                raise EvalError("division of non-integers")
        case Neg(s):
            sv = evalInEnv(env,s)
            if type(sv) is int:
                return -sv
            else:
                raise EvalError(f"negation operator requires an integer operand, but got {s}")

        # binding/variable forms 
        case Name(n):
            v = lookupEnv(n, env)
            if v is None:
                raise EvalError(f"unbound name {n}")
            return v
        case Let(n,defexpr,bodyexpr):
            v = evalInEnv(env, defexpr)
            newEnv = extendEnv(n, v, env)
            return evalInEnv(newEnv, bodyexpr)

        # comparison forms
        case Eq(l,r):
            lv, rv = evalInEnv(env, l), evalInEnv(env, r)
            if type(lv) != type(rv):
                return False
            return lv == rv
        case Lt(l,r):
            lv, rv = evalInEnv(env,l), evalInEnv(env,r)
            if type(lv) is int and type(rv) is int:
                return lv < rv
            else:
                raise EvalError(f"lt operator requires two integer operands, but got {l} and {r}")
        
        # conditional forms
        case If(cond, then_branch, else_branch):
            condv = evalInEnv(env, cond)
            if type(condv) is bool:
                if condv:
                    return evalInEnv(env, then_branch)
                else:
                    return evalInEnv(env, else_branch)
            else:
                raise EvalError(f"if operator requires a boolean condition, but got {cond}")
        # literals
        case Lit(v):
            return v     
     
        # string operator forms 
        case Concat(l,r):
            lv, rv = evalInEnv(env,l), evalInEnv(env,r)
            if type(lv) is Str and type(rv) is Str:
                return Str(lv.value + rv.value)
            else:
                raise EvalError(f"concat operator requires two string operands, but got {l} and {r}")
        case Replace(target, old, new):
            target, old, new = evalInEnv(env, target), evalInEnv(env, old), evalInEnv(env, new)
            if not all(isinstance(x, Str) for x in (target, old, new)):
                raise EvalError("Replace requires strings")
            return Str(target.value.replace(old.value, new.value, 1))
        case LetFun(name, param, funbody, letbody):
            clo = Closure(param, funbody, env)
            newEnv = extendEnv(name, clo, env)
            return evalInEnv(newEnv, letbody)
        case App(funexpr, actualarg):
            funval = evalInEnv(env, funexpr)
            if not isinstance(funval, Closure):
                raise EvalError(f"application of non-function {funexpr}")
            argval = evalInEnv(env, actualarg)
            newEnv = extendEnv(funval.param, argval, funval.env)
            return evalInEnv(newEnv, funval.body)
        case _:
            raise EvalError(f"unknown expression {e}")
