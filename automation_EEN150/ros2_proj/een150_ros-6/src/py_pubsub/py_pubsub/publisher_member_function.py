# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from geometry_msgs.msg import Twist, Vector3
import math


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        timer_period = 0.2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0.0

    def timer_callback(self):
        # a = 3
        t = self.i 
        x = 0.8 #0.1+t/100
        # y = math.e**t * math.sin(t*a)

        lin_vec = Vector3(x = x, y = 0.0, z =  0.0)
        ang_vec = Vector3(x = 0.0, y = 0.0, z =  math.radians(90 - t/4)) # z = rads, 
        msg = Twist(linear = lin_vec, angular=ang_vec)
        #msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        #self.get_logger().info('%s' % msg.angular.z)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
