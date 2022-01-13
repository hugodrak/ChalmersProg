import pytest
from predicates.state import State
from predicates.guards import Eq, Not, And, Or, from_str
from predicates.actions import Assign, Inc, Dec, Next
from predicates.errors import NextException


def test_action_assign():
    """
    This test checks the assign action that creates a new state where the
    value of the variable is updated either to a given value,
    or to the value from another variable, 
    """
    s1 = State(v1 = False, v2 = True, v3 = "open")
    a1 = Assign("v1", "hej") # updates v1 to "hej"
    a2 = Assign("v1", "v3") # updates v1 to "open"

    s1_next = a1.next(s1)
    s2_next = a2.next(s1)

    assert s1_next.get("v1") == "hej"
    assert s1_next.get("v3") == "open"

    a3 = Assign("foo", "v3")
    with pytest.raises(NextException) as e:
        a3.next(s1)

def test_action_inc():
    """
    This test checks the Inc action that creates a new state where the
    value of the variable is incremented
    """
    s1 = State(v1 = 1, v2 = True, v3 = "open")
    a1 = Inc("v1", 1) # updates v1 to 2
    a2 = Inc("v1", 5) # updates v1 to 6
    

    s1_next = a1.next(s1)
    s2_next = a2.next(s1)

    assert s1_next.get("v1") == 2
    assert s2_next.get("v1") == 6

    a3 = Inc("v3", 5)
    with pytest.raises(NextException) as e:
        a3.next(s1)
    a4 = Inc("v5", 5)
    with pytest.raises(NextException) as e:
        a4.next(s1)
    
def test_action_dec():
    """
    This test checks the Dec action that creates a new state where the
    value of the variable is decremented
    """
    s1 = State(v1 = 1, v2 = True, v3 = "open")
    a1 = Dec("v1", 1)
    a2 = Dec("v1", 5)

    s1_next = a1.next(s1)
    s2_next = a2.next(s1)

    assert s1_next.get("v1") == 0
    assert s2_next.get("v1") == -4
    
    a3 = Dec("v3", 5)
    with pytest.raises(NextException) as e:
        a3.next(s1)
    a4 = Dec("v5", 5)
    with pytest.raises(NextException) as e:
        a4.next(s1)

def test_action_next():
    """
    This test checks the Next action that creates a new state where the
    value of the variable is changed to the next value in a tuple
    """
    s1 = State(v1 = 1, v2 = True, v3 = "opened")
    domain = ("closed", "opening", "opened", "closing")
    a1 = Next("v3", domain)

    s1_next = a1.next(s1)
    s2_next = a1.next(s1_next)
    s3_next = a1.next(s2_next)

    assert s1_next.get("v3") == "closing"
    assert s2_next.get("v3") == "closed"
    assert s3_next.get("v3") == "opening"
    
    a2 = Next("v1", domain)
    with pytest.raises(NextException) as e:
        a2.next(s1)
    a3 = Next("v5", domain)
    with pytest.raises(NextException) as e:
        a3.next(s1)
