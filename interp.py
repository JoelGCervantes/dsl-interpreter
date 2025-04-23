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
            | strLit | Concat | Length


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
class strLit():
    value: str
    def __str__(self) -> str:
        return f"{self.value}"

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
        case Or(l,r):
            return evalInEnv(env,l) or evalInEnv(env,r)
        case Add(l,r):
            return evalInEnv(env,l) + evalInEnv(env,r)
        case Sub(l,r):
            return evalInEnv(env,l) - evalInEnv(env,r)
        case Mul(l,r):
            lv = evalInEnv(env,l)
            rv = evalInEnv(env,r)
            return lv * rv
        case Div(l,r):
            lv = evalInEnv(env,l)
            rv = evalInEnv(env,r)
            if rv == 0:
                raise EvalError("division by zero")
            return lv // rv
        case Neg(s):
            return - (evalInEnv(env,s))
        case Lit(i):
            return i
        case Name(n):
            v = lookupEnv(n, env)
            if v is None:
                raise EvalError(f"unbound name {n}")
            return v
        case Let(n,d,b):
            v = evalInEnv(env, d)
            newEnv = extendEnv(n, v, env)
            return evalInEnv(newEnv, b)
