from typing import Tuple, List
import pytest
from predicates.state import State
from predicates import guards, actions
from graphs.transition import Transition
from graphs.graph import Edge, Vertex, Graph
from graphs.factory import graph_factory

# ---------------------------------------------------------------------------
# ...
# ---------------------------------------------------------------------------

def setup() -> Tuple[(Graph, List[Vertex], List[Edge], Vertex, Vertex, Vertex, Vertex, Edge, Edge, Edge, Edge, Edge)]:
    """This method creates the test graph that we will use"""
    initial_state = State(a = 0)
    t1 = Transition("t1", guards.from_str("a == 0"), actions.from_str("a += 1"))
    t2 = Transition("t2", guards.from_str("a == 1"), actions.from_str("a += 1"))
    t3 = Transition("t3", guards.from_str("a == 0"), actions.from_str("a <- 2"))
    t4 = Transition("t4", guards.from_str("a == 2"), actions.from_str("a -= 1"))
    t5 = Transition("t5", guards.from_str("a == 2"), actions.from_str("a += 1"))


    g = graph_factory(initial_state, [t1, t2, t3, t4, t5])

    # and we also include the correct edges and vertices

    # this is how you should name your vertices in the graph
    # check so that this is actually true
    s0 = Vertex.from_state(State(a = 0))
    s1 = Vertex.from_state(State(a = 1))
    s2 = Vertex.from_state(State(a = 2))
    s3 = Vertex.from_state(State(a = 3))
    e1 = Edge("t1", s0, s1) # you can also use Edge.from_states("t1", State(a = 0), State(a = 1))
    e2 = Edge("t2", s1, s2)
    e3 = Edge("t3", s0, s2)
    e4 = Edge("t4", s2, s1)
    e5 = Edge("t5", s2, s3)

    return (
        g, 
        [s0, s1, s2, s3],
        [e1, e2, e3, e4, e5],
        s0,
        s1,
        s2,
        s3,
        e1,
        e2,
        e3,
        e4,
        e5
    )



def test_make_me_a_graph():
    """
    A graph should be created based on a set of transitions and a state using the 
    graph factory. So to make this test pass, you need to implement the function 
    graph_factory in the file factory.py.
    """
    (g,vs, es, s0, s1, s2, s3, e1, e2, e3, e4, e5) = setup()
    g.print_from_sources(5)
    assert g

def test_outgoing():
    """
    test the outgoing method on the graph so that the correct edges are going out
    from the correct vertices
    """
    (g,vs, es, s0, s1, s2, s3, e1, e2, e3, e4, e5) = setup()

    outgoing = g.outgoing(s0)

    # to be able to compare the result from your method, it needs to 
    # be sorted so the order of the edges is the same as my test list
    assert sorted(outgoing) == [e1, e3]

def test_outgoing_2():
    """
    test some more outgoing from other vertices
    """
    (g,vs, es, s0, s1, s2, s3, e1, e2, e3, e4, e5) = setup()

    o1 = g.outgoing(s1)
    o2 = g.outgoing(s2)
    o3 = g.outgoing(s3)

    assert sorted(o1) == [e2]
    assert sorted(o2) == [e4, e5]
    assert sorted(o3) == []

def test_incoming():
    """
    test the incoming method on the graph so that the correct edges are coming in
    from the correct vertices
    """
    (g,vs, es, s0, s1, s2, s3, e1, e2, e3, e4, e5) = setup()

    incoming = g.incoming(s1)

    # to be able to compare the result from your method, it needs to 
    # be sorted so the order of the edges is the same as ny test list
    assert sorted(incoming) == [e1, e4]

def test_incoming_2():
    """
    test some more incoming from other vertices
    """
    (g,vs, es, s0, s1, s2, s3, e1, e2, e3, e4, e5) = setup()

    i0 = g.incoming(s0)
    i2 = g.incoming(s2)
    i3 = g.incoming(s3)

    assert sorted(i0) == []
    assert sorted(i2) == [e2, e3]
    assert sorted(i3) == [e5]

def test_successor():
    """
    test the successor method so that the correct successor vertices are 
    connected correctly
    """
    (g,vs, es, s0, s1, s2, s3, e1, e2, e3, e4, e5) = setup()

    succ = g.successor(s0)

    assert sorted(succ) == [s1, s2]

def test_predecessor():
    """
    test the predecessor method so that the correct predecessor vertices are 
    connected correctly
    """
    (g,vs, es, s0, s1, s2, s3, e1, e2, e3, e4, e5) = setup()

    pred = g.predecessor(s1)

    assert sorted(pred) == [s0, s2]


def test_from_path():
    """
    test the from_path function, that takes in a start vertex and then follows a list of edges to follows.
    Returns the final vertex in the sequence if all edges exists. Otherwise None
    """
    (g,vs, es, s0, s1, s2, s3, e1, e2, e3, e4, e5) = setup()

    v1 = g.from_path(s0, ["t1", "t2"])
    v2 = g.from_path(s2, ["t4", "t2", "t5"])
    v3 = g.from_path(s1, ["t2", "t4"])
    v4 = g.from_path(s1, ["t2", "t7", "t1"])
    v5 = g.from_path(s3, [])

    assert v1 == s2
    assert v2 == s3
    assert v3 == s1
    assert v4 == None
    assert v5 == None

def test_from_path_2():
    """
    test the from_path method so that the correct vertex is reached when
    following a path from a vertex
    """
    (g,vs, es, s0, s1, s2, s3, e1, e2, e3, e4, e5) = setup()

    the_goal = g.from_path(s0, [e1.name, e2.name, e5.name])
    assert the_goal == s3

    the_goal = g.from_path(s1, [e2.name, e4.name])
    assert the_goal == s1

    the_goal = g.from_path(s1, [e2.name, e4.name, e3.name, e2.name])
    assert the_goal == None


def test_source_vertices():
    """
    test the predecessor method so that the correct predecessor vertices are 
    connected correctly
    """
    (g,vs, es, s0, s1, s2, s3, e1, e2, e3, e4, e5) = setup()

    sources = g.source_vertices()

    assert sources == [s0]


def test_sink_vertices():
    """
    test the predecessor method so that the correct predecessor vertices are 
    connected correctly
    """
    (g,vs, es, s0, s1, s2, s3, e1, e2, e3, e4, e5) = setup()

    sinks = g.sink_vertices()

    assert sinks == [s3]