from dataclasses import dataclass

@dataclass(frozen=True)
class NotInStateException(Exception):
    """
    This exception is raised when someone is trying to get the value of a variable from 
    the state that do not exists
    """
    message: str


@dataclass(frozen=True)
class NextException(Exception):
    """
    This exception is raised when a next function can not be executed du to that the variable 
    value is not of the the correct type of is missing in the state
    """
    message: str