import pytest
from predicates.state import State
from predicates import guards
from predicates.guards import Eq, Not, And, Or, Beq
from predicates import actions
from predicates.actions import Assign, Inc, Dec, Next

def test_parser():
    res = guards.from_str('a && (b == c)')
    g = And(Beq('a'), Eq('b', 'c'))

    s1 = State(a = True, b = "foo", c = "foo")
    s2 = State(a = True, b = "foo", c = "bar")

    assert res.eval(s1) and not res.eval(s2)
    assert isinstance(res, And)
    assert str(g) == str(res)

def test_parser_or():
    res = guards.from_str('a || (b == c)')
    g = Or(Beq('a'), Eq('b', 'c'))

    s1 = State(a = True, b = "foo", c = "foo")
    s2 = State(a = True, b = "foo", c = "bar")
    s3 = State(a = False, b = "foo", c = "bar")

    assert res.eval(s1) and res.eval(s2) and not res.eval(s3)
    assert isinstance(res, Or)
    assert str(g) == str(res)

def test_parser_more():
    res = guards.from_str('!a && (b || c || d) && (d != False)')
    g = And(Not(Beq('a')), Or(Beq('b'), Beq('c'), Beq('d')), Not(Eq('d', False)))

    s1 = State(a = False, b = True, c = False, d = True)
    s2 = State(a = True, b = True, c = False, d = True)

    print('result')
    print(res)

    assert res.eval(s1) and not res.eval(s2)
    assert isinstance(res, And)
    assert str(g) == str(res)

def test_parser_action():
    res = actions.from_str("a <- hej, b <- c, d <- {x, y, z}")
    a = (Assign('a', 'hej'), Assign('b', 'c'), Next('d', ('x', 'y', 'z')))

    assert str(res) == str(a)

def test_parser_action_more():
    res = actions.from_str("d <- {x, y, z}, a -= 2, b += 3")
    a = (Next('d', ('x', 'y', 'z')), Dec('a', 2), Inc('b', 3))

    assert str(res) == str(a)

def test_parser_true_false_assign():
    res = actions.from_str("d <- {x, y, z}, !a, b")
    a = (Next('d', ('x', 'y', 'z')), Assign('a', False), Assign('b', True))

    assert str(res) == str(a)

def test_guards_actions_equal_and_hash():
    x = guards.And(*(guards.Beq('a'), guards.Beq('b')))

    assert guards.from_str("a && b") == guards.from_str("a && b")
    assert guards.from_str("a && b") == x
    assert hash(guards.from_str("a && b")) == hash(guards.from_str("a && b"))
    assert hash(guards.from_str("a && b")) == hash(x)

    x = (actions.Assign("a", False), actions.Assign("c", True))
    assert tuple(actions.from_str("!a, c")) == x
    assert actions.from_str("!a, c") == actions.from_str("!a, c")
    assert hash(tuple(actions.from_str("!a, c"))) == hash(tuple(actions.from_str("!a, c")))