# Starting from a premade ubuntu docker file that include ros2
FROM kristoferb/spdesktop_ros2:galactic

# installing some packages 
RUN DEBIAN_FRONTEND=noninteractive apt-get update -qqy \
    && DEBIAN_FRONTEND=noninteractive apt-get install -qqy \
    nano \
    wget
   
# installing the messages that we need for controlling the simulation
COPY handlers_msgs/ /msgs/
RUN cd /msgs &&\ 
    rm COLCON_IGNORE &&\
    . /opt/ros/galactic/setup.sh &&\
    colcon build

# installing the python requirements and sourcing ros when we are running
COPY requirements.txt /
RUN pip install -r /requirements.txt &&\
    echo "source /opt/ros/galactic/setup.bash" >> ~/.bashrc &&\
    echo "source /msgs/install/setup.bash" >> ~/.bashrc

