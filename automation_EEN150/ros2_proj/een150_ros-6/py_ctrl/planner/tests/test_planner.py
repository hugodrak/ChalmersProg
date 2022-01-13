from typing import Tuple, List
import pytest
from predicates.state import State
from predicates import guards, actions
from predicates.guards import AlwaysTrue, AlwaysFalse
from model.model import the_model, Model
from model.operation import Operation, Transition
from planner.plan import plan

# ---------------------------------------------------------------------------
# Test for the planner. The first tests can be used before the model is
# created but the last ones needs to be updated since they also check your model
# ---------------------------------------------------------------------------

g = guards.from_str
a = actions.from_str


def test_simple_planner_0():
    """
    This test checks the implementation of the planner with a simple model
    """
    initial_state = State(
        v1 = False,
        v2 = 0
    )

    o1 = Operation(
        name=f"o1", 
        precondition=Transition("pre", g("v2 == 0"), ()), 
        postcondition=Transition("post", AlwaysTrue(), a(f"v2 += 1")), 
        effects=(),
    )
    o2 = Operation(
        name=f"o2", 
        precondition=Transition("pre", g("v2 == 1"), ()), 
        postcondition=Transition("post", AlwaysTrue(), a(f"v2 += 3")), 
        effects=(),
    )
    o3 = Operation(
        name=f"o3", 
        precondition=Transition("pre", g("v2 == 1"), ()), 
        postcondition=Transition("post", AlwaysTrue(), a(f"v2 += 1")), 
        effects=(),
    )
    o4 = Operation(
        name=f"o4", 
        precondition=Transition("pre", g("v2 == 4"), ()), 
        postcondition=Transition("post", AlwaysTrue(), a(f"v2 <- 2")), 
        effects=(),
    )

    simple_model = Model(initial_state, {
        o1.name: o1,
        o2.name: o2,
        o3.name: o3,
        o4.name: o4,
    })

    goal = g("v2 == 2")
    p = plan(initial_state, goal, simple_model)
    assert p != None
    assert len(p) != 0
    assert p == [o1.name, o3.name]




def test_simple_planner_1():
    """
    This test checks the implementation of the planner with a simple model
    """
    initial_state = State(
        v1 = False,
        v2 = 0
    )

    o1 = Operation(
        name=f"o1", 
        # enabled when v1 is false
        precondition=Transition("pre", g("!v1"), ()), 
        # the guard of the postcondition is only used when running the operation, not when planning
        postcondition=Transition("post", AlwaysTrue(), a(f"v1")), 
        # the effects are only used when planning to simulate changes of sensors
        effects=(),
    )
    o2 = Operation(
        name=f"o2", 
        precondition=Transition("pre", g("v1 && v2 == 0"), ()),
        postcondition=Transition("post", AlwaysTrue(), a(f"v2 += 1")),
        effects=(),
    )
    o3 = Operation(
        name=f"o3", 
        precondition=Transition("pre", g("v1 && v2 == 0"), ()),
        postcondition=Transition("post", AlwaysTrue(), a(f"v2 += 2")),
        effects=(),
    )
    o4 = Operation(
        name=f"o4", 
        precondition=Transition("pre", g("v1 && v2 == 2"), ()),
        postcondition=Transition("post", AlwaysTrue(), a(f"v2 += 1")),
        effects=(),
    )
    o5 = Operation(
        name=f"o5", 
        precondition=Transition("pre", g("v1"), ()),
        postcondition=Transition("post", AlwaysTrue(), a(f"v2 <- 0")),
        effects=(),
    )
    simple_model = Model(initial_state, {
        o1.name: o1,
        o2.name: o2,
        o3.name: o3,
        o4.name: o4,
        o5.name: o5,
    })

    goal = g("v2 == 3")
    p = plan(initial_state, goal, simple_model)
    assert p != None
    assert len(p) != 0
    assert p == [o1.name, o3.name, o4.name]

    goal = g("v2 == 1")
    p = plan(initial_state, goal, simple_model)
    assert p == [o1.name, o2.name]

def test_simple_planner_2():
    """
    This test checks the implementation of the planner with a simple model
    """
    initial_state = State(
        v1 = False,
        v2 = 0
    )
    ops = {}
    for i in range(100):
        ops[f"o{i}"] = Operation(
            name=f"o{i}", 
            # enabled when v1 is false
            precondition=Transition("pre", g("!v1"), ()), 
            # the guard of the postcondition is only used when running the operation, not when planning
            postcondition=Transition("post", AlwaysTrue(), a(f"v1")), 
            # the effects are only used when planning to simulate changes of sensors
            effects=(),
        )
    


    ops["final"] = Operation(
        name=f"final", 
        precondition=Transition("pre", g("v1 && v2 == 0"), ()),
        postcondition=Transition("post", AlwaysTrue(), a(f"v2 += 1")),
        effects=(),
    )
    model = Model(initial_state, ops)

    goal = g("v2 == 1")
    p = plan(initial_state, goal, model)
    print(p)
    assert p != None
    assert len(p) == 2
    assert p[1] == "final"

def test_simple_planner_3():
    """
    This test checks the implementation of the planner with a simple model
    """
    initial_state = State(
        v1 = False,
        v2 = 0
    )
    ops = {}
    for i in range(100):
        ops[f"o{i}"] = Operation(
            name=f"o{i}", 
            # enabled when v1 is false
            precondition=Transition("pre", g(f"v2 == {i}"), ()), 
            # the guard of the postcondition is only used when running the operation, not when planning
            postcondition=Transition("post", AlwaysTrue(), a(f"v2 +=1")), 
            # the effects are only used when planning to simulate changes of sensors
            effects=(),
        )

    ops["final"] = Operation(
        name=f"final", 
        precondition=Transition("pre", g("v1 && v2 == 0"), ()),
        postcondition=Transition("post", AlwaysTrue(), a(f"v2 += 1")),
        effects=(),
    )
    model = Model(initial_state, ops)

    goal = g("v2 == 100")
    p = plan(initial_state, goal, model, 120)
    print(p)
    assert p != None
    assert len(p) == 100



# Use this test when you are working with the model 
def test_planner_real_model_1():
    """This method creates the test the planner that you will use for just a simple case"""
    m = the_model()
    
    goal = g("r1_act == home")
    assert plan(m.initial_state, goal, m) == []
    
    
    goal = g("r1_act == pos1")
    # This plan should only include one operation. Change the dummy name below to 
    # the name of the operation that you are using
    assert plan(m.initial_state, goal, m) == ["r1_to_pos1"]
    
    goal = g("r1_act == foo")
    # Your planner should not find any path, but it will take a long time
    # if you have depth 30 so increase this only sometimes to test
    assert plan(m.initial_state, goal, m, 5) == None
    
    # here you should create more tests to check your model ...


def test_planner_real_model_two():
    m = the_model()
    # write a goal so that the cubes are at different positions than the inital ones
    goal = g("pos1_col == blue_cube && pos2_col == red_cube && pos3_col == green_cube")
    p = plan(m.initial_state, goal, m)
    assert p != None
        
    for o in p:
        print(o)

    # add all operations that should be parts of your solution.
    # Look at the printout and see if it is correct and than add them here
    should_find = set(['r1_to_pos2', 'r1_grasp_pos2', 'r2_to_pos1', 'r2_grasp_pos1', 'r1_to_home', 'r2_to_pos2', 
                        'r2_release_pos2', 'r1_to_pos1', 'r1_release_pos1'])
    assert set(p) == should_find

def test_planner_real_model_three():
    m = the_model()
    # write a goal so that the cubes are at different positions than the inital ones
    goal = g("pos1_col == green_cube && pos2_col == red_cube && pos3_col == blue_cube")
    p = plan(m.initial_state, goal, m)
    assert p != None
        
    for o in p:
        print(o)

    # add all operations that should be parts of your solution.
    # Look at the printout and see if it is correct and than add them here
    should_find = set(['r1_to_pos2', 'r1_grasp_pos2', 'r2_to_pos1', 'r2_grasp_pos1', 'r1_to_home', 'r2_to_pos2', 'r2_release_pos2', 
                        'r2_to_pos3', 'r2_grasp_pos3', 'r2_to_pos1', 'r2_release_pos1', 'r1_to_pos3', 'r1_release_pos3'])
    assert set(p) == should_find

def test_planner_real_model_three_2():
    m = the_model()
    # write a goal so that the cubes are at different positions than the inital ones
    goal = g("pos1_col == blue_cube && pos2_col == red_cube && pos3_col == green_cube")
    p = plan(m.initial_state, goal, m)
    assert p != None

    s = m.initial_state
    new_state = s
    for path in p:
        op = m.operations[path]
        if op.eval(new_state):
            new_state = op.next_planning(new_state)


    res = new_state.get("pos1_col") == "blue_cube" and new_state.get("pos2_col") == "red_cube" and new_state.get("pos3_col") == "green_cube"
    assert res == True
    # ------------------------
    goal2= g("pos1_col == green_cube && pos2_col == blue_cube && pos3_col == red_cube")
    p2 = plan(new_state, goal2, m)
    assert p2 != None

    new_state2 = new_state
    for path in p2:
        op = m.operations[path]
        if op.eval(new_state2):
            new_state2 = op.next_planning(new_state2)


    res2 = new_state2.get("pos1_col") == "green_cube" and new_state2.get("pos2_col") == "blue_cube" and new_state2.get("pos3_col") == "red_cube"
    assert res2 == True

