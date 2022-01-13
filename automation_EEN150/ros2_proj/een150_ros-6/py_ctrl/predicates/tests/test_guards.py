import pytest
from predicates.state import State
from predicates import guards
from predicates.guards import Eq, Beq, Not, And, Or
from predicates.errors import NotInStateException



def test_guards_beq():
    """
    Testing the class Beq. This class is already implemented and you can get a feeling for 
    how the guards are implemented and how to use the state.
    """

    s1 = State(v1 = False, v2 = True, v3 = "open")
    s2 = State(v1 = True, v2 = True, v3 = "open")
    eq = Beq("v1")
    eq2 = Beq("v3")
    assert not eq.eval(s1)
    assert eq.eval(s2)
    assert not eq2.eval(s1) # false if not boolean
    
    eq3 = Beq("v10")
    with pytest.raises(NotInStateException) as e:
        eq3.eval(s1)

    # these lasts tests checks the _eq__ and __hash__ implementation. Should just work
    assert Beq("v1") == Beq("v1") 
    assert hash(Beq("v1")) == hash(Beq("v1"))
    assert Beq("v1") != Beq("v2") 
    assert hash(Beq("v1")) != hash(Beq("v2"))


def test_guards_eq():
    """
    Testing the class Eq
    """

    s1 = State(v1 = False, v2 = True, v3 = "open")
    s2 = State(v1 = True, v2 = True, v3 = "open")
    eq = Eq("v1", "v2")
    eq2 = Eq("v3", "open")
    assert not eq.eval(s1)
    assert eq.eval(s2)
    assert eq2.eval(s1)
    
    eq3 = Eq("v10", "open")
    with pytest.raises(NotInStateException) as e:
        eq3.eval(s1)

    # these lasts tests checks the _eq__ and __hash__ implementation. Should just work
    assert Eq("v1", "v2") == Eq("v1", "v2") 
    assert hash(Eq("v1", "v2")) == hash(Eq("v1", "v2"))
    assert Eq("v1", "v2") != Eq("v1", "hej") 
    assert hash(Eq("v1", "v2")) != hash(Eq("v1", "hej"))



def test_guards_not():
    """
    Testing the class Not
    """

    s1 = State(v1 = False, v2 = True, v3 = "open")
    eq = Eq("v1", False)
    eq2 = Eq("v3", "closed")
    assert not Not(eq).eval(s1)
    assert Not(eq2).eval(s1)
    eq3 = Eq("v10", "open")
    with pytest.raises(NotInStateException) as e:
        Not(eq3).eval(s1)

    # these lasts tests checks the _eq__ and __hash__ implementation. 
    assert Not(eq) == Not(eq) 
    assert hash(Not(eq)) == hash(Not(eq))
    assert Not(eq) != Not(eq2) 
    assert hash(Not(eq)) != hash(Not(eq2))

def test_guards_and():
    """
    Testing the class And
    """

    s1 = State(v1 = False, v2 = True, v3 = "open")
    s2 = State(v1 = True, v2 = True, v3 = "open")
    eq = Eq("v1", "v2")
    eq2 = Eq("v3", "open")
    eq3 = Eq("v1", True)
    eq4 = Eq("v2", True)
    assert not And(eq, eq2, eq3).eval(s1)
    assert And(eq, eq2, eq3, eq4).eval(s2)

    eq5 = Eq("v10", "open")
    with pytest.raises(NotInStateException) as e:
        And(eq, eq2, eq3, eq4, eq5).eval(s2)

    # these lasts tests checks the _eq__ and __hash__ implementation. 
    assert And(eq, eq2) == And(eq, eq2)
    assert hash(And(eq, eq2)) == hash(And(eq, eq2))
    assert And(eq, eq2) != And(eq, eq3)
    assert hash(And(eq, eq2)) != hash(And(eq, eq3))

def test_guards_or():
    """
    Testing the class Or
    """

    s1 = State(v1 = False, v2 = True, v3 = "open")
    eq = Eq("v1", "v2")
    eq2 = Eq("v3", "open")
    eq3 = Eq("v1", True)
    eq4 = Eq("v2", True)
    eq5 = And(eq, eq2, eq3)
    assert not Or(eq, eq3, eq5).eval(s1)
    assert Or(eq, eq2, eq3, eq4).eval(s1)

    eq6 = Eq("v10", "open")
    with pytest.raises(NotInStateException) as e:
        Or(eq, eq2, eq3, eq4, eq6).eval(s1)

    # these lasts tests checks the _eq__ and __hash__ implementation. 
    assert Or(eq, eq2) == Or(eq, eq2)
    assert hash(Or(eq, eq2)) == hash(Or(eq, eq2))
    assert Or(eq, eq2) != Or(eq, eq3)
    assert hash(Or(eq, eq2)) != hash(Or(eq, eq3))


def test_guards_complex():
    """
    This should just work if the guards are correct
    """
    s1 = State(a = False, b = True, c = False, d = True)
    s2 = State(a = True, b = True, c = False, d = True)
    
    g = guards.from_str('!a && (b || c || d) && (d != False)')
    assert g.eval(s1) and not g.eval(s2)

    # these lasts tests checks the _eq__ and __hash__ implementation. 
    assert g == g
    assert hash(g) == hash(g)
    g2 = guards.from_str('!a && (b || c || d) && (d != True)')
    assert g != g2
    assert hash(g) != hash(g2)