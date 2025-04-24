'''
Joel Garcia-Cervantes 
CS358 Principles of Programming Languages
Spring 2025

This file contains AST node definitions for expressions, an eval method for interpreting
expressions to values, and a run method for showing values to the use. It is part of Milestone 1 for the
term project.

'''
from dataclasses import dataclass

type Value = int | bool | Str

@dataclass
class Str():
    value: str
    def __str__(self) -> str:
        return f"{self.value}"
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Str):
            return self.value == other.value
        return False


type Expr = Or | And | Not | boolLit \
            | intLit | Add | Sub | Mul | Div | Neg \
            |  Let | Name \
            | Eq | Lt | If \
            | Concat | Length


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
class boolLit():
    value: bool
    def __str__(self) -> str:
        return f"{self.value}"


@dataclass
class intLit():
    value: int
    def __str__(self) -> str:
        return f"{self.value}"

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
class Eq: # equality 
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} == {self.right})"

@dataclass # less than 
class Lt:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} < {self.right})"

@dataclass
class If: # if expression 
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
class Length():
    subexpr: Expr
    def __str__(self) -> str:
        return f"(length {self.subexpr})"


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
            lv, rv = evalInEnv(env,l), evalInEnv(env,r)
            if isinstance(lv, bool) and isinstance(rv, bool):
                return lv or rv
            else:
                raise EvalError(f"or operator requires two boolean operands, but got {l} and {r}")
        case And(l,r):
            lv, rv = evalInEnv(env,l), evalInEnv(env,r)
            if isinstance(lv, bool) and isinstance(rv, bool):
                return lv and rv
            else:
                raise EvalError(f"and operator requires two boolean operands, but got {l} and {r}")
        case Not(s):
            sv = evalInEnv(env,s)
            if isinstance(sv, bool):
                return not sv
            else:
                raise EvalError(f"not operator requires a boolean operand, but got {s}")
            
        # arithmetic(int) expression forms
        case Add(l,r):
            lv, rv = evalInEnv(env,l), evalInEnv(env,r)
            if isinstance(lv, int) and isinstance(rv, int):
                return lv + rv
            elif isinstance(lv, Str) and isinstance(rv, Str):
                return Str(lv.value + rv.value)
            else:
                raise EvalError(f"add operator requires two integer or string operands, but got {l} and {r}")
        case Sub(l,r):
            lv, rv = evalInEnv(env,l), evalInEnv(env,r)
            if isinstance(lv, int) and isinstance(rv, int):
                return lv - rv
            else:
                raise EvalError(f"sub operator requires two integer operands, but got {l} and {r}")
        case Mul(l,r):
            lv, rv = evalInEnv(env,l), evalInEnv(env,r)
            if isinstance(lv, int) and isinstance(rv, int):
                return lv * rv
            else:
                raise EvalError(f"mul operator requires two integer operands, but got {l} and {r}")
        case Div(l,r):
            lv = evalInEnv(env,l)
            rv = evalInEnv(env,r)
            if rv == 0:
                raise EvalError("division by zero")
            if isinstance(lv, int) and isinstance(rv, int):
                return lv // rv
        case Neg(s):
            sv = evalInEnv(env,s)
            if isinstance(sv, int):
                return -sv
            else:
                raise EvalError(f"neg operator requires an integer operand, but got {s}")

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
            lv, rv = evalInEnv(env,l), evalInEnv(env,r)
            if isinstance(lv, bool) and isinstance(rv, bool):
                return lv == rv
            elif isinstance(lv, int) and isinstance(rv, int):
                return lv == rv
            elif isinstance(lv, Str) and isinstance(rv, Str):
                return lv == rv
            else:
                raise EvalError(f"eq operator requires two operands of the same type, but got {l} and {r}")
        case Lt(l,r):
            lv, rv = evalInEnv(env,l), evalInEnv(env,r)
            if isinstance(lv, int) and isinstance(rv, int):
                return lv < rv
            else:
                raise EvalError(f"lt operator requires two integer operands, but got {l} and {r}")
        
        # conditional forms
        case If(cond, then_branch, else_branch):
            condv = evalInEnv(env, cond)
            if isinstance(condv, bool):
                if condv:
                    return evalInEnv(env, then_branch)
                else:
                    return evalInEnv(env, else_branch)
            else:
                raise EvalError(f"if operator requires a boolean condition, but got {cond}")
        # literals
        case boolLit(v):
            return v
        case intLit(v):
            return v
        case Str(v):
            return Str(v)
        
        # string operator forms 
        case Concat(l,r):
            lv, rv = evalInEnv(env,l), evalInEnv(env,r)
            if isinstance(lv, Str) and isinstance(rv, Str):
                return Str(lv.value + rv.value)
            else:
                raise EvalError(f"concat operator requires two string operands, but got {l} and {r}")
        case Length(s):
            sv = evalInEnv(env,s)
            if isinstance(sv, Str):
                return len(sv.value)
            else:
                raise EvalError(f"length operator requires a string operand, but got {s}")
        case _:
            raise EvalError(f"unknown expression {e}")
