'''
Joel Garcia-Cervantes 
CS358 Principles of Programming Languages
Spring 2025

This file contains AST node definitions for expressions, an eval method for interpreting
expressions to values, and a run method for showing values to the use. It is part of Milestone 1 for the
term project.

'''
from dataclasses import dataclass

type Literal = int

type Expr = Or | And | Not | boolLit \
            | intLit | Add | Sub | Mul | Div | Neg \
            |  Let | Name \
            | Eq | Lt | If


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
class Eq:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} == {self.right})"

@dataclass
class Lt:
    left: Expr
    right: Expr
    def __str__(self) -> str:
        return f"({self.left} < {self.right})"

@dataclass
class If:
    cond: Expr
    then_branch: Expr
    else_branch: Expr
    def __str__(self) -> str:
        return f"(if {self.cond} then {self.then_branch} else {self.else_branch})"



