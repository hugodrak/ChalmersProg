import pytest
from predicates.state import State
from predicates import guards, actions
from model.operation import Transition, Operation
from predicates.errors import NextException

# ---------------------------------------------------------------------------
# Some tests to check the implementation of operations and transitions. 
# they are already implemented
# ---------------------------------------------------------------------------


def test_operation():
    pre = Transition("pre", guards.Eq("a", 0), (actions.Assign("a", 1),))
    post = Transition("post", guards.Eq("b", 1), (actions.Assign("a", 2),))
    effect = actions.Assign("b", 2)
    o = Operation("o", pre, post, (effect, ))

    s = State(a = 0, b = 0)
    eval = o.eval(s)
    start = o.start(s)
    is_completed_false = o.is_completed(start)
    c_state = actions.Assign("b", 1).next(start)
    is_completed = o.is_completed(c_state)
    complete = o.complete(c_state)
    next_planning = o.next_planning(s)
    eval_false = o.eval(complete)

    assert(eval)
    assert(not eval_false)
    assert(start == State(a = 1, b = 0, o = "e"))
    assert(not is_completed_false)
    assert(is_completed)
    assert(complete == State(a = 2, b = 1, o = "i"))
    assert(next_planning == State(a = 2, b = 2))



def test_transition():
    """

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
    