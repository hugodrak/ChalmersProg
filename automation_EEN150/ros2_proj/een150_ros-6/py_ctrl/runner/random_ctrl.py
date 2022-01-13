# ---------------------------------------------------------------------------
# The random ctrl can be used for testing a model, even if it is not complete.
# It will run one random operation at the time and wait for the response from 
# the simulation.
# ---------------------------------------------------------------------------

from typing import Optional, Tuple, List
import random
from predicates.state import State
from model.model import the_model, Model, from_goal_to_goal
from planner.plan import plan
from model.operation import Operation
from predicates.state import State


import rclpy
from rclpy.node import Node

from std_msgs.msg import String, Bool
from handlers_msgs.msg import CubeState



class Runner(Node):
    
    def __init__(self):
        super().__init__('the_runner')
        self.model: Model = the_model()
        self.state: State = self.model.initial_state

        # Subscribing to the UR3s (r1) actual position
        self.create_subscription(
            msg_type = String,
            topic='/ia_planning/r1/act_pos',
            callback = self.r1_act_callback,
            qos_profile = 10)

        # Subscribing to the UR5s (r2) actual position
        self.create_subscription(
            msg_type = String,
            topic='/ia_planning/r2/act_pos',
            callback = self.r2_act_callback,
            qos_profile = 10)

        # Subscribing to the UR3s (r1) signal if the gripper is closed
        self.create_subscription(
            msg_type = Bool,
            topic='/ia_planning/r1/gripping',
            callback = self.r1_gripping_callback,
            qos_profile = 10)

        # Subscribing to the UR5s (r2) signal if the gripper is closed
        self.create_subscription(
            msg_type = Bool,
            topic='/ia_planning/r2/gripping',
            callback = self.r2_gripping_callback,
            qos_profile = 10)

        # Publishing a reference position to the UR3s (r1),
        # telling it where to go
        self.pub_r1_ref = self.create_publisher(
            msg_type=String,
            topic = '/ia_planning/r1/ref_pos',
            qos_profile=10
        )

        # Publishing a command to the UR3s (r1),
        # telling it to close the gripper
        self.pub_r1_grip = self.create_publisher(
            msg_type=Bool,
            topic = '/ia_planning/r1/grip',
            qos_profile=10
        )

        # Publishing a reference position to the UR5s (r2),
        # telling it where to go
        self.pub_r2_ref = self.create_publisher(
            msg_type=String,
            topic = '/ia_planning/r2/ref_pos',
            qos_profile=10
        )

        # Publishing a command to the URs (r1),
        # telling it to close the gripper
        self.pub_r2_grip = self.create_publisher(
            msg_type=Bool,
            topic = '/ia_planning/r2/grip',
            qos_profile=10
        )

        # the ticker that defines the "scan-cycle"
        self.timer = self.create_timer(0.1, self.ticker)
            

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
        prev_state = self.state
        self.state = tick_the_random_runner(self.state, self.model)

        # uncomment to print the state for troubleshooting
        if prev_state != self.state:
            print("")
            print(f"changed state:")
            for k, v in set(self.state.items()) - set(prev_state.items()):
                print(f"{k}: {v}")
            print(f"")
        

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


def tick_the_random_runner(state: State, model: Model) -> State:
    """
    This function will run the operations based on a plan that are located in the state
    This will just execute one transition at the time
    """

    running_ops: List[Operation] = [o for name, o in model.operations.items() if state.get(name) == "e"]
    next_state = state

    if not running_ops:
        enabled_ops = [o for _, o in model.operations.items() if o.precondition.eval(state)]
        if not enabled_ops:
            print("No operations are enabled or running in this state!")
            return state
        
        o = random.choice(enabled_ops)
        next_state = o.start(state)
        print(f"Operation {o.name} started!")

    else:
        ops_can_complete = [o for o in running_ops if o.postcondition.eval(state)]
        if ops_can_complete:
            next_state = state
            for o in ops_can_complete:
                next_state = o.complete(next_state)
                print(f"Operation {o.name} completed!")

    return next_state



def run():
    rclpy.init()
    runner = Runner()
    rclpy.spin(runner)
    runner.destroy_node()
    rclpy.shutdown()

