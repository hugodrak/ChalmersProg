from dataclasses import dataclass
from typing import Optional, Tuple
from predicates.state import State
from predicates.guards import Guard
from predicates.actions import Action
from predicates.errors import NextException

# A Transition class includes a name of the transition, a guard predicate 
# and a list of actions.
# The class should implement both the eval method and the next method
# in the same way as the guards and the actions. Look at the test so the 
# method parameters and return types are correct.
# 
#    
@dataclass(frozen=True, order=True)
class Transition(object):
    name: str
    guard: Guard
    actions: Tuple[Action]

    def eval(self, state: State) -> bool:
        return self.guard.eval(state)

    def next(self, state: State) -> State:
        curr_state = state
        if not self.guard.eval(curr_state):
                raise NextException(f"Guard is not True")
        
        for action in self.actions:
            curr_state = action.next(curr_state)
        return curr_state


        

