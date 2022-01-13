import queue
from model.model import Model
from typing import List, Optional
from predicates.state import State
from  predicates.guards import Guard
from queue import Queue
# goal is to both do breadth first and deapth first. Hyp is that breadth is better
import time

import heapq

class MyHeap(object):
   def __init__(self, initial=None, key=lambda x:x):
       self.key = key
       self.index = 0
       if initial:
           self._data = [(key(item), i, item) for i, item in enumerate(initial)]
           self.index = len(self._data)
           heapq.heapify(self._data)
       else:
           self._data = []

   def push(self, item):
       heapq.heappush(self._data, (self.key(item), self.index, item))
       self.index += 1

   def pop(self):
       return heapq.heappop(self._data)[2]
    
   def empty(self):
        if len(self._data) == 0:
            return True
        return False


time_lookup = {"2_h_1": 6, "2_h_2": 5, "2_h_3": 6,
               "1_h_1": 4, "1_h_2": 3, "1_h_3": 4,
               "1_2": 1, "1_3": 2, "2_3": 1, "2_1": 1, "3_1": 2, "3_2": 1, "0": 0} # these values are based on that r2(bigger) has a longer arm


def calc_cost(s1_org, s2_org): # maybe op inst of s2
    s1 = s1_org.state.copy()
    s2 = s2_org.state.copy()
    if 'runner_goal' in s1.keys():
        del s1['runner_goal']
    if 'runner_goal' in s2.keys():
        del s2['runner_goal']
    set1 = set(s1.items())
    set2 = set(s2.items())
    diffing_keys = [x[0] for x in set1 ^ set2]
    key = "0"
    d_key = ""
    r_no = "1"
    if "r1_act" in diffing_keys:
        d_key = "r1_act"
        r_no = "1"
    elif "r2_act" in diffing_keys:
        d_key = "r2_act"
        r_no = "2"
    elif "r2_gripping" in diffing_keys or "r1_gripping" in diffing_keys:
        return 2 # time for gripping/ releasing

    if d_key:
        v1 = s1.get(d_key)
        v2 = s2.get(d_key)
        p1 = ""
        p2 = ""
        if "home" in v1:
            p1 = "h"
            
        elif v1[-1] in ["1", "2", "3"]:
            p1 = v1[-1]
        
        if "home" in v2:
            p2 = "h"
            
        elif v2[-1] in ["1", "2", "3"]:
            p2 = v2[-1]

        if p1 == "h":
            key = f"{r_no}_{p1}_{p2}"
        elif p2 == "h":
            key = f"{r_no}_{p2}_{p1}"
        else:
            key = f"{p1}_{p2}"



        cost = time_lookup[key]
        return cost
    return 0

    

def BFS_plan(state, goal, model, max_depth):
    visited = [state]
    q = Queue()
    q.put((state, [])) # state, path

    while q.qsize() > 0:
        s = q.get()
        if len(s[1]) > max_depth:
            return None

        if goal.eval(s[0]):
                    return s[1]

        for name, op in model.operations.items():
            if op.eval(s[0]):
                next_state = op.next_planning(s[0])
                if next_state not in visited:
                    visited.append(next_state)
                    q.put([next_state, s[1]+ [name]])

    return None


#maybe use weight as fktn of length, or execution time? grasp takes 1, pos1 to pos2 takes 1?
# def djikstra_plan(state, goal, model, max_depth):
#     visited = [state]
#     q = PriorityQueue()
#     q.put((0, (state, []))) # state, path, cost

#     while not q.empty():
#         try:
#             s_tot = q.get() # if prio is eq then error due to x < y comp on dicts
#         except:
#             print(q.queue)
#             q.get()
#             raise ValueError("ffff")
#         if s_tot:
#             s = s_tot[1]
#         else:
#             raise ValueError("wrong s")
#         if len(s[1]) > max_depth:
#             return None

#         if goal.eval(s[0]):
#                     return s[1]

#         for name, op in model.operations.items():
#             if op.eval(s[0]):
#                 next_state = op.next_planning(s[0])
#                 if next_state not in visited:
#                     cost = calc_cost(s[0], next_state)
#                     visited.append(next_state)
#                     q.put((cost, (next_state, s[1] + [name])))

#     return None

def djikstra_plan(state, goal, model, max_depth):
    visited = [state]
    q = MyHeap(key= lambda x: x[0])
    q.push((0, (state, []))) # state, path, cost

    while not q.empty():
        s_tot = q.pop() # if prio is eq then error due to x < y comp on dicts
        s_cost, s = s_tot
        if len(s[1]) > max_depth:
            return None
        
        if goal.eval(s[0]):
                    return s[1]

        for name, op in model.operations.items():
            if op.eval(s[0]):
                next_state = op.next_planning(s[0])
                if next_state not in visited:
                    cost = calc_cost(s[0], next_state)
                    visited.append(next_state)
                    q.push((s_cost + cost, (next_state, s[1] + [name])))

    return None


# def BFS_tree(state, goal, ops, max_depth):
#     stack = []
#     visited = []

#     steps = []
#     stack.append(state)

#     steps.append([])

#     while stack:
#         if len(steps) > 0 and len(steps[-1]) > 0:
#             steps[-1] = [steps[-1][-1]]

#         if len(steps) > max_depth:
#             return None
        
#         if steps[-1]:
#             steps.append([])

#         s = stack.pop(0)

#         for op in ops:
#             if op.eval(s):
#                 next_state = op.next_planning(s)

#                 if goal.eval(next_state):
#                     steps[-1] = [op.name]
#                     return [x[0] for x in steps]

#                 if next_state not in visited:
#                     visited.append(next_state)
#                     stack.append(next_state)
#                     steps[-1].append(op.name)


def plan(state: State, goal: Guard, model: Model, max_depth: int = 20) -> Optional[List[str]]:
    """
    Find a sequence of operations to reach the goal from the given state or
    return None if you can not find a plan. Use max_depth to stop searching when you have more than
    max_depth steps in the path. 

    In planning you should use the eval() method of the operation to check if it is enabled and 
    the next_planning() to execute both pre, post and effect actions. While planning, no operations
    will run in parallell so they complete directly. We are only interested in finding the minimum 
    number of operations to reach the goal, not the shortest time.

    In the runner, there is a mode to pre-start operations, but that should not be considered while planning
    """
    ## Check if goal already is fulfilled
    if goal.eval(state):
        return []
    # t1 = time.time()
    #d = BFS_plan(state, goal, model, max_depth)
    # t2 = time.time()
    d = djikstra_plan(state, goal, model, max_depth)
    # t3 = time.time()
    # print("BFD:", t2-t1, "DJIK:", t3-t2)
    return d
