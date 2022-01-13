import pytest
from predicates.state import State
from predicates import guards, actions
from graphs.transition import Transition
from predicates.errors import NextException

# ---------------------------------------------------------------------------
# ...
# ---------------------------------------------------------------------------

def test_creating_a_transition():
    """
    this test should pass, and checks the class Transition in the transition.py file. 
    The Transition __init__ takes a name, a guard and a list of actions. It is important
    that you do not just store the list of actions as a list inside the class, but instead 
    as a tuple. You can convert it with tuple(list). This is because a list can not be hashed, so 
    it will be hard to implement the hash function. See Next for inspiration.
    Observe that the dataclass already implements an __init__ method. So this will probably already work
    """
    t1 = Transition("T1", guards.from_str("a && b"), actions.from_str("!a, c"))
    t1_v2 = Transition("T1", guards.from_str("a && b"), actions.from_str("!a, c"))
    print(t1)

    assert t1 # check that the Transition could be created 
    assert t1 == t1_v2 # check that the __eq__ is implemented
    assert hash(t1) == hash(t1_v2) # check that the __hash__ is implemented

def test_transition_eval():
    """
    The transition can be fired when its guard is true, which i checked with the eval function
    You have to add the method eval to Transition
    """
    t1 = Transition("T1", guards.from_str("a && b"), actions.from_str("!a, c"))
    print(t1)
    s1 = State(a = False, b = True, c = False)
    s2 = State(a = True, b = True, c = False)

    assert not t1.eval(s1)
    assert t1.eval(s2)

def test_transition_eval_2():
    """
    The transition can be fired when its guard is true, which i checked with the eval function
    """
    t1 = Transition("T1", guards.from_str("a == 0"), actions.from_str("a += 1"))
    t2 = Transition("T2", guards.from_str("(a == 0) && (b == 'hej')"), actions.from_str("a += 1"))
    print(t1)
    s1 = State(a = 0, b = "hej", c = "foo")
    s2 = State(a = 1, b = "hej", c = "bar")

    assert t1.eval(s1)
    assert not t1.eval(s2)
    assert t2.eval(s1)
    assert not t2.eval(s2)

def test_transition_next():
    """
    The transition can be fired when its guard is true, If it is true, a new state is created
    where each action, one at the time, updates the state. Next should raise an NextException
    if next is called when its guard is not true.
    You have to add the next method to Transition
    """
    t1 = Transition("T1", guards.from_str("a && b"), actions.from_str("!a, c"))
    print(t1)
    s1 = State(a = True, b = True, c = False)
    s2 = State(a = False, b = True, c = False)

    s1_next = t1.next(s1)
    assert s1_next == State(a = False, b = True, c = True)

    with pytest.raises(NextException) as e:
        t1.next(s2)
 
def test_transition_ordering():
    """
    It is important that the actions are applied to the state in order.
    """
    t1 = Transition("T1", guards.from_str("b"), actions.from_str("a += 1, c, a += 1, a += 1, !c,  a += 2"))
    print(t1)
    s = State(a = 0, b = True, c = False)
    s_next = t1.next(s)
    assert (s_next.get("a") == 5) and not s_next.get("c")
    