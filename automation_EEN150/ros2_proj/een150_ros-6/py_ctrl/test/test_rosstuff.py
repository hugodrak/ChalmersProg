import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor

from std_msgs.msg import String

from planner import plan


class MinimalSubscriber(Node):
    res = False
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        print("We got it")
        self.res = True


class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        print('Publishing: "%s"' % msg.data)
        self.i += 1


def testing():
    rclpy.init()
    try:
        talker = MinimalPublisher()
        listener = MinimalSubscriber()

        # Runs all callbacks in the main thread
        executor = SingleThreadedExecutor()
        # Add imported nodes to this executor
        executor.add_node(talker)
        executor.add_node(listener)

        try:
            # Execute callbacks for both nodes as they become ready
            executor.spin_once(timeout_sec=1)
            executor.spin_once(timeout_sec=1)
            executor.spin_once(timeout_sec=1)
            executor.spin_once(timeout_sec=1)
        finally:
            executor.shutdown()
            listener.destroy_node()
            talker.destroy_node()

    finally:
        rclpy.shutdown()

    assert(listener.res)


