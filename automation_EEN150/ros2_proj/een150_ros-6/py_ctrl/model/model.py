from dataclasses import dataclass
from typing import List, Optional, Dict
from model.operation import Operation, Transition
from predicates.state import State
import predicates.guards
import predicates.actions
from predicates.guards import AlwaysFalse, AlwaysTrue, Guard
from handlers_msgs.msg import CubeState

@dataclass
class Model(object):
    initial_state: State
    operations: Dict[str, Operation]

    def __post_init__(self):
        ops = {o: "i" for o in self.operations}
        self.initial_state = self.initial_state.next(**ops)


g = predicates.guards.from_str
a = predicates.actions.from_str

def the_model() -> Model:
    """
    Here you should create the variables and operations that can be used both for planning to reach the goal 
    and running the simulator. I have made some operations and some dummy examples to get you going. But you
    probably have to modify this and the dummy operations, you can remove.
    Observe: The name of a variable can not be the same as any value since we have the variable_or_value strings. 
    The initial state of the cubes are: poses = {"pos1": "red_cube", "pos2": "blue_cube", "pos3": "green_cube"}
    """
    
    initial_state = State(
        # control variables / output / qx
        r1_ref = "home",            #{home, pos1, pos2, pos3}
        r1_grip = False,

        r2_ref = "home",            #{home, pos1, pos2, pos3}
        r2_grip = False,

        # measured variables / input /  ix
        r1_act = "home",            #{home, pos1, pos2, pos3}
        r1_gripping = False,

        r2_act = "home",            #{home, pos1, pos2, pos3}
        r2_gripping = False,

        # estimated below
        r1_holding = False,
        r2_holding = False,
        pos1_col = "red_cube",
        pos2_col = "blue_cube",
        pos3_col = "green_cube",

        )

    # we will store all operations in this dict that will be part of the model
    ops = {}


    for rob in [1,2]:
        o_rob = 2 if rob == 1 else 1
        ops[f"r{rob}_to_home"] = Operation(
            name=f"r{rob}_to_home", 
            precondition=Transition("pre", g(f"(r{rob}_act != home)"), a(f"r{rob}_ref <- home")),
            postcondition=Transition("post", g(f"r{rob}_act == home"), ()),
            effects=a(f"r{rob}_act <- home")
        )

        for pos in [1,2,3]:

            ops[f"r{rob}_to_pos{pos}"] = Operation(
                name=f"r{rob}_to_pos{pos}",
                precondition=Transition("pre", g(f"r{rob}_act != pos{pos} && r{o_rob}_act != pos{pos} && (!r{rob}_gripping || (r{rob}_gripping && pos{pos}_col == None))"), a(f"r{rob}_ref <- pos{pos}")),
                postcondition=Transition("post", g(f"r{rob}_act == pos{pos}"), ()),
                effects=a(f"r{rob}_act <- pos{pos}")
            )
            
            ops[f"r{rob}_grasp_pos{pos}"] = Operation(
                name=f"r{rob}_grasp_pos{pos}", 
                precondition=Transition("pre", g(f"r{rob}_act == pos{pos} && !r{rob}_gripping"), a(f"r{rob}_grip")),
                postcondition=Transition("post", g(f"r{rob}_gripping"), a(f"r{rob}_holding <- pos{pos}_col") + a(f"pos{pos}_col <- None")),
                effects= a(f"r{rob}_gripping")
            )
            
            ops[f"r{rob}_release_pos{pos}"] = Operation(
                name=f"r{rob}_release_pos{pos}",  
                precondition=Transition("pre", g(f"r{rob}_act == pos{pos} && r{rob}_gripping"), a(f"!r{rob}_grip")),
                postcondition=Transition("post", g(f"!r{rob}_gripping"), a(f"pos{pos}_col <- r{rob}_holding") + a(f"r{rob}_holding <- None")),
                effects= a(f"!r{rob}_gripping")
            )

    return Model(initial_state, ops)





    
def from_goal_to_goal(cube_goal: CubeState) -> Guard:
    """
    Create a goal predicate based on where the cubes should be placed.
    CubeState is the message that is received from ros and it includes where we want the 
    cube colors to be. The possible colors are "red_cube", "blue_cube", 
    "green_cube"
    """
    print(cube_goal)
    pos1: str = cube_goal.pos1
    pos2: str = cube_goal.pos2
    pos3: str = cube_goal.pos3
    goal = g(f"pos1_col == {pos1} && pos2_col == {pos2} && pos3_col == {pos3}")
    return goal
