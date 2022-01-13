# a simple script to send a goal. Change the order to try different goals
# you probably need to set the permission on this file in the docker 
# inside the planner folder write: chmod +x ./send_goal.bash
ros2 topic pub --once /goal \
    handlers_msgs/msg/CubeState \
    "{'pos1':'blue_cube', 'pos2':'red_cube', 'pos3':'green_cube'}" 