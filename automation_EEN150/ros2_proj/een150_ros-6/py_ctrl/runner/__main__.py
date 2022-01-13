import runner.ctrl

if __name__ == '__main__':
    # run in terminal when venv is sourced: python3 -m runner
    runner.ctrl.run()
    # ros2 topic pub /goal handlers_msgs/msg/CubeState "{'pos1':'green_cube', 'pos2':'blue_cube', 'pos3':'red_cube'}" 

