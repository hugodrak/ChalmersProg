from predicates.state import State
from predicates import guards, actions
from predicates.guards import Eq, Beq, And, Or
from predicates.actions import Assign, Inc, Dec, Next

if __name__ == '__main__':
    # here you can write code to test variius things when you want to have nice printouts
    # run in terminal when venv is sourced: python3 -m predicates

    s1 = State(a = False, b = True, c = False, d = True)
    s2 = State(a = True, b = True, c = False, d = True)
    
    g = guards.from_str('!a && (b || c || d) && (d != False)')
    print(f"A nice guard: {g}")
    print(f"And it is : {g.eval(s1)}, in state s1")
    print(f"And it is : {g.eval(s2)}, in state s2")
