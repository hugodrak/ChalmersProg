from typing import Optional, Tuple, List
from predicates.state import State
from model.model import the_model, Model, from_goal_to_goal
from planner.plan import plan
from model.operation import Operation
from predicates.state import State


import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Bool
from handlers_msgs.msg import CubeState

# ---------------------------------------------------------------------------
# ...
# ---------------------------------------------------------------------------


runner_goal: str = "runner_goal"
runner_plan: str = "runner_plan"
step_in_plan: str = "step_in_plan"
plan_status: str = "plan_status"

# publish a goal:
# ros2 topic pub /goal handlers_msgs/msg/CubeState "{'pos1':'blue_cube', 'pos2': 'red_cube', 'pos3':'green_cube'}"

class Runner(Node):
    
    def __init__(self):
        super().__init__('the_runner')
        self.model: Model = the_model()
        self.state: State = self.model.initial_state
        self.upd_state(runner_goal, None)
        self.upd_state(runner_plan, None)
        self.upd_state(step_in_plan, None)
        self.upd_state(plan_status, None)

        # Subscribing to the goal
        self.create_subscription(
            msg_type = CubeState,
            topic = 'goal',
            callback = self.goal_callback,
            qos_profile = 10)

        self.create_subscription(
            msg_type = String,
            topic='/ia_planning/r1/act_pos',
            callback = self.r1_act_callback,
            qos_profile = 10)

        self.create_subscription(
            msg_type = String,
            topic='/ia_planning/r2/act_pos',
            callback = self.r2_act_callback,
            qos_profile = 10)

        self.create_subscription(
            msg_type = Bool,
            topic='/ia_planning/r1/gripping',
            callback = self.r1_gripping_callback,
            qos_profile = 10)

        self.create_subscription(
            msg_type = Bool,
            topic='/ia_planning/r2/gripping',
            callback = self.r2_gripping_callback,
            qos_profile = 10)

        self.pub_r1_ref = self.create_publisher(
            msg_type=String,
            topic = '/ia_planning/r1/ref_pos',
            qos_profile=10
        )
        self.pub_r1_grip = self.create_publisher(
            msg_type=Bool,
            topic = '/ia_planning/r1/grip',
            qos_profile=10
        )
        self.pub_r2_ref = self.create_publisher(
            msg_type=String,
            topic = '/ia_planning/r2/ref_pos',
            qos_profile=10
        )
        self.pub_r2_grip = self.create_publisher(
            msg_type=Bool,
            topic = '/ia_planning/r2/grip',
            qos_profile=10
        )

        self.timer = self.create_timer(0.1, self.ticker)


    def goal_callback(self, msg: CubeState):
        """
        Here the goal comes in from ros and if we do not have a goal, or if the goal is 
        new, it will reset the runner so it will replan.
        """
        goal = self.state.get(runner_goal)
        if goal != msg:
            print(f"We got a new goal: {from_goal_to_goal(msg)}")
            self.upd_state(runner_goal, msg)
            self.upd_state(runner_plan, None)
            self.upd_state(step_in_plan, None)
            self.upd_state(plan_status, None)
            


    def r1_act_callback(self, msg: String):
        self.upd_state("r1_act", msg.data)

    def r2_act_callback(self, msg: String):
        self.upd_state("r2_act", msg.data)

    def r1_gripping_callback(self, msg: Bool):
        self.upd_state("r1_gripping", msg.data)

    def r2_gripping_callback(self, msg: Bool):
        self.upd_state("r2_gripping", msg.data)

    def upd_state(self, key: str, value):
        self.state = self.state.next(**{key: value})

    def ticker(self):
        g = self.state.get(runner_goal)
        p = self.state.get(runner_plan)
        if not g:
            print("waiting for a goal")
            return
        if not p and not self.state.get(plan_status):
            # if we have a new goal, let us replan
            goal = from_goal_to_goal(g)
            new_p = plan(self.state, goal, self.model, 30)
            self.upd_state(runner_plan, new_p)
            print(f"The new goal: {goal}")
            print(f"and computed this plan: {new_p}")

        prev_state = self.state

        # here we call the ticker. Change the pre_start parameter to true when
        # you want to prestart
        self.state = tick_the_runner(self.state, self.model, True)

        if prev_state != self.state:
            print(f"")
            for k, v in self.state.items():
                print(f"{k}: {v}")
            print(f"")
        

        # below, we are publishing the command variables to the simulation via ros
        msg = String()
        msg.data = self.state.get("r1_ref")
        self.pub_r1_ref.publish(msg)

        msg.data = self.state.get("r2_ref")
        self.pub_r2_ref.publish(msg)
        
        msg = Bool()
        msg.data = self.state.get("r1_grip")
        self.pub_r1_grip.publish(msg)

        msg.data = self.state.get("r2_grip")
        self.pub_r2_grip.publish(msg)


def tick_the_runner(state: State, model: Model, pre_start: bool) -> State:
    """
    This function will run the operations based on a plan that are located in the state
    This will just execute one transition at the time
    """
    the_plan: list[str] = state.get(runner_plan)    
    if not the_plan:
        return state.next(plan_status="No plan in state")
    
    current_step_in_plan: int = state.get(step_in_plan)
    if not current_step_in_plan:
        # we have not started executing the plan so we start at position 0 in the plan
        current_step_in_plan = 0
        state = state.next(**{step_in_plan: current_step_in_plan})
    
    plan_length = len(the_plan)
    if plan_length <= current_step_in_plan:
        # we are done with the plan and will stop executing and we also
        # reset the current plan so we do not tries to run the same plan again
        return state.next(plan_status="done", runner_plan = None, step_in_plan = None)

    # check what operation we are / should be executing
    current_op_name = the_plan[current_step_in_plan]
    current_op_state: str = state.get(current_op_name)
    current_op: Operation = model.operations[current_op_name]

    next_step = current_step_in_plan + 1

    if current_op_state == "i" and current_op.eval(state): # The operation can be started
        next_state = current_op.start(state)
    elif current_op_state == "i": # the operation should be started but is not enabled
        next_state = state.next(plan_status=f"waiting for op {current_op_name} to be enabled. pre: {current_op.precondition}")
    elif current_op.is_completed(state): # the operation has completed and we can take a step in the plan
        next_state = current_op.complete(state)
        next_state = next_state.next(step_in_plan=next_step, plan_status=f"completing step {current_step_in_plan}")
    elif current_op_state == "e": # the operation is executing, let's check if we can prestart the next
        if not pre_start:
            next_state = state.next(plan_status=f"waiting for op to complete")
        elif plan_length > next_step and model.operations[the_plan[next_step]].eval(state):
            next_state = model.operations[the_plan[next_step]].start(state).next(
                plan_status=f"pre_starting {next_step}"
            )
        else:
            next_state = state
    else:
        next_state = state.next(plan_status="doing nothing")
        
    return next_state



def run():
    rclpy.init()
    runner = Runner()
    rclpy.spin(runner)
    runner.destroy_node()
    rclpy.shutdown()

