from predicates.state import State
from predicates import guards, actions
from graphs.transition import Transition
from graphs.graph import Edge, Vertex, Graph
from graphs.factory import graph_factory

if __name__ == '__main__':
    # here you can write code to test variius things when you want to have nice printouts
    # run in terminal when venv is sourced: python3 -m graphs

    initial_state = State(a = 0)
    t1 = Transition("t1", guards.from_str("a == 0"), actions.from_str("a += 1"))
    t2 = Transition("t2", guards.from_str("a == 1"), actions.from_str("a += 1"))
    t3 = Transition("t3", guards.from_str("a == 0"), actions.from_str("a <- 2"))
    t4 = Transition("t4", guards.from_str("a == 2"), actions.from_str("a -= 1"))
    t5 = Transition("t5", guards.from_str("a == 2"), actions.from_str("a += 1"))


    g = graph_factory(initial_state, [t1, t2, t3, t4, t5])

    g.print_from_sources(10)
    print(g.source_vertices())
    print(g.sink_vertices())