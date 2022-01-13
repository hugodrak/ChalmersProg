from typing import List, Optional
from graphs.transition import Transition
from predicates.state import State
from graphs.graph import Graph, Vertex, Edge


def graph_factory(state: State, transitions: List[Transition]) -> Graph:
    """
    In this method you should create a graph that represent the "execution" of
    the transitions from the initial state. I.e. start in the initial state and
    evaluate what transitions that are enabled in that state. call next on these transitions
    so new states are created, from where you continue to take new transitions to new states.
    Observe that there may be loops taking you back to an already visited state, so if
    you do not handle that, your algorithm may get stuck in an endless loop.

    The name of each vertex in the graph (nodes) should be named as the states since each
    vertex is directly related to one state. So use Vertex.from_state(...) or the Edge.from_states(...)
    class methods. The name of the edges in your graph should be the same name as the transition that can take you
    from the tail vertex (state) to the head vertex (state). That means that different edges can have the
    same name in the graph since one transition can be enabled in multiple states

    You need to decide how you will represent the graph inside the graph class
    and then generate all the objects you need.
    """

    stack = []
    visited = []
    edge_list = []
    stack.append(state)
    while stack:
        s = stack.pop(0) # take out one and remove from list
        for t in transitions:
            if t.eval(s):
                next_state = t.next(s)
                edge = Edge.from_states(t.name, s, next_state)
                edge_list.append(edge)
                if next_state not in visited:
                    visited.append(next_state)
                    stack.append(next_state)

    return Graph(edge_list)
