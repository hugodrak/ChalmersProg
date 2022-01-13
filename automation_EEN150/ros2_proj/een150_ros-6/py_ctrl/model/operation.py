from dataclasses import dataclass
from typing import ClassVar, List, Optional, Tuple
import predicates.guards
from predicates.state import State
from predicates.guards import Eq, Guard, guards
from predicates.actions import Action, Assign
from predicates.errors import NextException


@dataclass(frozen=True, order=True)
class Transition(object):
    name: str
    guard: Guard
    actions: Tuple[Action, ...]
    """
    A Transition class includes a name of the transition, a guard predicate 
    and a list of actions.
    This transition also include a next_planning that can be used by the operation while planning
    since it does not raise an exception when it is not enabled. This is used to run the postcondition
    in the operation without the need for the guard to be true.
    """

    def eval(self, state: State) -> bool:
        return self.guard.eval(state)

    def next(self, state: State) -> State:
        if not self.eval(state):
            raise NextException(f"Calling next on transition {self.name}, when eval is false")
        
        s = state
        for a in self.actions:
            s = a.next(s)
        return s

    def next_planning(self, state: State) -> State:
        s = state
        for a in self.actions:
            s = a.next(s)
        return s


        
@dataclass(frozen=True, order=True)
class Operation(object):
    name: str
    precondition: Transition
    postcondition: Transition
    effects: Tuple[Action, ...]
    """
    The operation represent a task that will take some time before completion, and is a good
    abstraction that can be used for both planning and control. The operation has a state variable
    op = "i" # when it is in its initial state, and op = "e" when it is executing.

    The precondition is a Transition that defines a guard when the operation is allowed to start 
    and a set of actions that triggers state changes that are used for starting the resources that
    the operation controls. For example pre: 
    !robot && act_pos == atPickPos && !gripping / robot; grip;
    where !robot checks so no other operation is using the robot, act_pos check that the robot is 
    in position to pick, and !gripping that we are not gripping. The action robot and grip changes 
    theses variables to True. 

    The postcondition is a Transitions that defines a guard when the operation has completed and a 
    list of actions. If the operation should update some estmated variables that are not measured,
    these should be changed here. For example
    post: gripping / !robot; part_in_gripper <- part_at_pick_pos; part_at_pick_pos <- empty
    where gripping is a measured variable from the gripper resource and part_in_gripper and 
    part_at_pick_pos are estimated variables that we may use to keep track of the parts

    The effect are used to emulate changes of measured variables when planning

    """
    
    
    def eval(self, state: State) -> bool:
        """Check if the operation can start. Should be used both when planning and running"""
        init = not state.contains(self.name) or Eq(self.name, "i").eval(state)
        return init and self.precondition.eval(state)

    def start(self, state: State) -> State:
        """Start the operation when running"""
        if not state.contains(self.name):
            state = state.next(**{self.name: "i"})
        a = Assign(self.name, "e")
        return a.next(self.precondition.next(state))

    def is_completed(self, state: State) -> bool:
        """check if the operation has completed while running"""
        return Eq(self.name, "e").eval(state) and self.postcondition.eval(state)

    def complete(self, state: State) -> State:
        """apply the post actions when running"""
        return self.postcondition.next(Assign(self.name, "i").next(state))

    def next_planning(self, state: State) -> State:
        """
        When planning, the guard of the postcondition may not become true since nothing will
        change the measured variables. Therefore, this method can be used that triggers the 
        actions of both the pre- and postconditions. The effects will also be applied so that
        other operations, that have measured variables in their guards, can start.
        """
        s = self.postcondition.next_planning(self.precondition.next_planning(state))
        for a in self.effects:
            s = a.next(s)
        return s

