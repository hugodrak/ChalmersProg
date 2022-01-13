# ---------------------------------------------------------------------------
# We will be learning how to use test-driven development in this course. You 
# have to implement code so that all tests pass, as well as implementing your 
# own tests. 
#
# 
# First, i will show you some tests where the implementation is already implemented. Try to 
# figure out how they work and try to understand the implementation of the state.
# ---------------------------------------------------------------------------

from predicates.errors import NotInStateException
import pytest
from predicates.state import State
from predicates.guards import Eq, Not, And, Or, from_str


def test_creating_a_state():
    """
    For this first test, the code is already implemented and you can look at the 
    implemented code in the State class.

    Testing the two ways of creating a state
    """
    state = State(v1 = False, v2 = True, v3 = "open") 
    dict = {"v1": False, "v2":True, "v3": "open"}
    state2 = State(**dict)
    assert state == state2
    
def test_state_equals():
    """
    Testing that the equals implementation works
    """
    s1 = State(v1 = False, v2 = True, v3 = "open") 
    s2 = State(v1 = False, v2 = True, v3 = "closed") 
    s3 = State(v1 = False, v2 = True, v3 = "open")
    assert s1 != s2
    assert s1 == s3
    assert s1 != State(foo = "bar")

def test_state_items():
    """
    Testing that the items function works
    """
    s1 = State(v1 = False, v2 = True, v3 = "open") 
    should_be = State(v1 = True, v2 = False, v3 = False) 

    # A boring way to iterate
    x = {}
    for variable, value in s1.items():
        x[variable] = not value
    assert State(**x) == should_be

    # a comprehension is much shorter and better
    x = {variable: not value for variable, value in s1.items() }
    assert State(**x) == should_be

    # Another way is the map function
    x = dict(map(lambda var_value: (var_value[0], not var_value[1]), s1.items())) 
    assert State(**x) == should_be



def test_state_getting_values():
    """
    This is the first test where the code is not implemented.
    This test check the get method in the State class and that it 
    is possible to get a value of a variable. If the variable exists
    in the state, it should be returned, else a NotInStateException 
    shall be raised.
    """
    s1 = State(v1 = False, v2 = True, v3 = "open") 

    assert s1.get("v1") == False
    assert s1.get("v1") != True
    with pytest.raises(NotInStateException) as e:
        s1.get("foo")
    assert s1.get("v3") == "open"



def test_next_state():
    """
    This is the first test where the code is not implemented. Try to understand 
    what is going on and then implement the method in the State class
    """
    s1 = State(v1 = False, v2 = True, v3 = "open")
    s2 = State(v1 = True, v2 = True, v3 = "open")
    
    res = s1.next(v1 = True)
    assert res == s2

def test_next_state_immutable():
    """
    Hopefully you found a way to make the previous test pass. This test will check
    so that your solution did not change the old state when creating the next state
    It is important later that each state can not be changed after it has been created, 
    since we need to store many states. This is called immutability.
    """

    s1 = State(v1 = False, v2 = True, v3 = "open")
    s2 = State(v1 = True, v2 = True, v3 = "open")

    res = s1.next(v1 = True)
    assert s1 != s2
