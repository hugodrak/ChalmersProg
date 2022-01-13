# -------------------------------------------------------------------------
# This files defines the various guard predicates that we will use
# (or will define them when you have fixed the missing parts)
# -------------------------------------------------------------------------

from typing import Any, Protocol, Tuple
from predicates.state import State
from dataclasses import dataclass
from predicates.errors import NotInStateException


class Guard(Protocol):
    """
    This is our Guard protocol, which we use in type hints for our duck-typing classes
    Read more about protocol: 
    https://docs.python.org/3/library/typing.html#typing.Protocol
    https://mypy.readthedocs.io/en/stable/protocols.html#simple-user-defined-protocols

    This is just a way for us to document for the users of our code what types we expect
    You do not really need to understand this, but it is a way for us to say that a method
    will return a Guard, which is any class that implement the eval(...) method.
    
    """
    def eval(self, state: State) -> bool:
        ...


@dataclass(frozen=True, order=True)
class AlwaysTrue:
    """
    A guard that is always true, for use in transitions
    """

    def eval(self, state: State) -> bool:
        return True

@dataclass(frozen=True, order=True)
class AlwaysFalse:
    """
    A guard that is always false, for use in transitions
    """

    def eval(self, state: State) -> bool:
        return False

@dataclass(frozen=True, order=True)
class Beq:
    bool_variable: str
    """
    Beq evaluate if a variable value is True or False
    If the state is {v1:False, v2:True}, then Beq(v1) is False and Beq(v2) is True
    This is already implemented so you will get a feeling for what is going on...
    """
    
    def eval(self, state: State) -> bool:
        """
        This guard evaluates to true if the value, that should be a boolean, is true or false
        This is an atomic proposition since it does not include other guards
        If the variable is not included in the state a NotInStateException will be raised
        """
        return state.get(self.bool_variable) == True


@dataclass(frozen=True, order=True)
class Eq:
    variable: str
    value_or_variable: Any
    """
    Eq evaluate if a variable value is equal to another value or another variable value
    E.g. v1 == "foo", v1 == v2. 
    If the state is {v1:"foo", v2:True}, then (v1 == "foo") is True and (v1 == v2) is False
    """

    def eval(self, state: State) -> bool:
        """
        This guard evaluates if the value of a variable is equal to a given value 
        or if a variable name is given, it is equal to that variables value.
        This is an atomic proposition since it does not include other guards
        If the variable is not included in the state a NotInStateException will be raised
        """
        x = state.get(self.variable)
        y = self.value_or_variable
        if self.value_or_variable in state.state:
            y = state.get(self.value_or_variable)

        return x == y




    


@dataclass(frozen=True, order=True)
class Not:
    guard: Guard
    """
    Not evaluate if another Guard is False, and in that case returns True
    If the state is {v1:False, v2:True}, then Not(Beq(v1)) is True and Not(Beq(v2)) is False
    """
    
    def eval(self, state: State) -> bool:
        """
        The NOT guard negates another guard. 
        This evaluates to true if the guard guard is false
        If the variable is not included in the state a NotInStateException will be raised
        """
        return not self.guard.eval(state)

@dataclass(frozen=True, order=True, init=False)
class And:
    guards: Tuple[Guard, ...]
    """
    The AND guard evaluates a list of other guards. 
    This evaluates to true if all guards in the list are true
    """
    
    def eval(self, state) -> bool:
        """
        The AND guard that takes a list of other guards. 
        This evaluates to true if all guards in the list are true
        NotInStateException will be raised if any of the guard fails
        """
        res = [g.eval(state) for g in self.guards]
        return all(res)

    def __init__(self, *args) -> None:
        """Override the init method in dataclass to handle args"""
        object.__setattr__(self, "guards", tuple(args))


@dataclass(frozen=True, order=True, init=False)
class Or:
    guards: Tuple[Guard, ...]
    """
    The Or guard evaluates a list of other guards. 
    This evaluates to true any of the guards in the list are true
    """
    
    def eval(self, state) -> bool:
        """
        The OR guard that takes a list of other guards.
        This evaluates to true if any of the guards in the list are true
        NotInStateException will be raised if any of the guard fails
        """
        res = [g.eval(state) for g in self.guards]
        return any(res)

    def __init__(self, *args) -> None:
        """Override the init method in dataclass to handle args"""
        object.__setattr__(self, "guards", tuple(args))





        

#--------------------------------------------
# below is a parser to simplify wring of guards. You do not need to 
# change anythng but can take a look how a text parser can be written. 
# See the test_parser.py for example how it works
#--------------------------------------------

from parsec import string, regex, generate, many, separated
import ast

whitespace = regex(r'\s+')
ignore = many(whitespace)
lexeme = lambda p: p << ignore  # skip all ignored characters.

eq = lexeme(string('=='))
neq = lexeme(string('!='))
not_sign = lexeme(string('!'))
and_sign = lexeme(string('&&'))
or_sign = lexeme(regex(r'\|\|'))
symbol = lexeme(regex(r'\w+'))
lparen = lexeme(string('('))
rparen = lexeme(string(')'))


@generate
def equals() -> Eq:
    """matches v1 == value, or v1 == v2"""
    key = yield symbol
    yield eq
    val = yield symbol
    try:
        val = ast.literal_eval(val)
    except ValueError as e:
        pass
    res = Eq(key, val)
    return res

@generate
def nequals() -> Not:
    """matches v1 != value, or v1 != v2"""
    key = yield symbol
    yield neq
    val = yield symbol
    try:
        val = ast.literal_eval(val)
    except ValueError as e:
        pass
    res = Not(Eq(key, val))
    return res

@generate
def bools() -> Beq:
    """matches v1"""
    key = yield symbol
    res = Beq(key)
    return res

@generate
def ands() -> And:
    """matches guard && guard && guard ..., where guard is one of the other generators"""
    values = yield separated(par ^ nots ^ equals ^ nequals ^ bools, and_sign, 2, 10) # type: ignore
    res = And(*values)
    return res

@generate
def ors() -> Or:
    """matches guard || guard || guard, where guard is one of the other generators"""
    values = yield separated(par ^ nots ^ equals ^ nequals ^ bools, or_sign, 2, 10) # type: ignore
    res = Or(*values)
    return res

@generate
def par() -> Guard:
    """matches (guard), where guard is one of the other generators"""
    yield lparen
    g = yield guards()
    yield rparen
    return g

@generate
def nots() -> Not:
    """matches !guard, where guard is either a paranthesis or a Beq"""
    yield not_sign
    g = yield par ^ bools # type: ignore
    return Not(g)


def guards() -> Guard:
    return ands ^ ors ^ par ^ nots ^ equals ^ nequals  ^ bools # type: ignore

def from_str(str) -> Guard:
    """This function will parse a str into a guard. There may be situation that is not handled though"""
    predicate = ignore >> guards()
    return predicate.parse(str)


