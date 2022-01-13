import pytest
from predicates.state import State
from predicates import guards, actions
from model.operation import Transition, Operation
from predicates.errors import NextException
from model.model import Model, the_model, from_goal_to_goal
from handlers_msgs.msg import CubeState

def test_model_creation():
    m = the_model()
    enabled_in_initial = [o for name, o in m.operations.items() if o.eval(m.initial_state)]
    assert len(enabled_in_initial) > 0


# write your own tests so that you know that the model you have created is the one you expected.
# for example, write a test for each operation so that it is enabled in the correct states and
# that it changes the state both when using next_planning and start and complete

def test_r1_to_home():
    m = the_model()
    ops = m.operations

    test_state = m.initial_state.next(r1_ref = "pos1", r1_act = "pos1")
    o = ops["r1_to_home"]
    
    after_start = o.start(test_state)
    not_completed = o.is_completed(after_start)
    completed = o.is_completed(after_start.next(r1_act = "home"))
    after_completed = o.complete(after_start.next(r1_act = "home"))
    
    assert o.eval(test_state)
    assert after_start == test_state.next(r1_ref = "home", r1_to_home = "e")
    assert not not_completed
    assert completed
    assert after_completed == after_start.next(r1_act = "home", r1_to_home = "i")
    
    after_planned = o.next_planning(test_state)
    assert after_planned == test_state.next(r1_ref = "home", r1_act = "home")


def test_some_operations():
    m = the_model()
    s = m.initial_state
    at_p1 = m.operations["r1_to_pos1"].next_planning(s)
    assert guards.Eq("r1_act", "pos1").eval(at_p1)



# Write your own tests to check the all the operations 

# Write your own tests to check the all the operations 
def test_some_operations_3():
    m = the_model()
    s = m.initial_state
    o1 = m.operations["r1_to_pos1"]
    o2 = m.operations["r1_grasp_pos1"]
    o3 = m.operations["r2_to_pos2"]
    o4 = m.operations["r2_grasp_pos2"]
    o5 = m.operations["r2_to_home"]
    o6 = m.operations["r1_to_pos2"]
    o7 = m.operations["r1_release_pos2"]
    new_state = s
    for op in [o1, o2, o3, o4, o5, o6, o7]:
        if op.eval(new_state):
            new_state = op.next_planning(new_state)
        else:
            assert False
    print(new_state)
    assert new_state.get("pos2_col") == "red_cube" 

def test_some_operations_4():
    m = the_model()
    s = m.initial_state
    o1 = m.operations["r2_to_pos2"]
    o2 = m.operations["r2_grasp_pos2"]
    o3 = m.operations["r2_to_pos3"]
    new_state = s
    for op in [o1, o2, o3]:
        if op.eval(new_state):
            new_state = op.next_planning(new_state)
    print(new_state)
    assert new_state.get("r2_ref") == "pos2" 

def test_goal_to_goal():
    # you need to implement the translation from the goal message to your way of tracking the cubes
    cube_goal = CubeState()
    cube_goal.pos1 = "red_cube"
    cube_goal.pos2 = "blue_cube"
    cube_goal.pos3 = "green_cube"

    goal = from_goal_to_goal(cube_goal)
    m = the_model()
    assert goal.eval(m.initial_state)
