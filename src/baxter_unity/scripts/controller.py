#!/usr/bin/env python

import rospy
from multiprocessing import JoinableQueue, Process

"""
Baxter Interface classes for easy access to ROS API
"""
from baxter_interface import (
    Limb,
    RobotEnable,
)

"""
Geometry messages required for the IKSolver Service
"""
from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Header,
) 

from baxter_core_msgs.msg import (
    JointCommand,
    EndpointState,
)

from sensor_msgs.msg import (
    JointState,
)

"""
Baxter IK Solver
"""
from baxter_core_msgs.srv import (
    SolvePositionIK as ik_solver
)

import time

class BaxterNode():
    def __init__(self, con_queue, can_queue):
        self.control_queue = con_queue
        self.cancel_queue = can_queue
        self.node = 'rsdk_baxter_unity'

        self._component_ids = {
            'left': ['left_e0', 'left_e1', 'left_s0', 'left_s1', 'left_w0', 'left_w1', 'left_w2'],
            'right': ['right_e0', 'right_e1', 'right_s0', 'right_s1', 'right_w0', 'right_w1', 'right_w2']
        }

        # IKSolver topics - Accepts sensor_msgs/JointState
        self.ik_topics = {
            'left': '/ExternalTools/left/PositionKinematicsNode/IKService',
            'right': '/ExternalTools/right/PositionKinematicsNode/IKService',
        }

        # JointCommand topics - Accepts baxter_core_msgs/JointCommand
        self.comm_topics = {
            'left': '/robot/limb/left/joint_command',
            'right': '/robot/limb/right/joint_command'
        }

        rospy Publishers for IKService topics
        self.ik_publishers = {
            'left': rospy.Publisher(
                self.ik_topics['left'], 
                sensor_msgs.msg.JointState, 
                queue_size = None,
                tcp_nodelay = True
            ),
            'right':  rospy.Publisher(
                self.ik_topics['right'],
                sensor_msgs.msg.JointState,
                queue_size = None,
                tcp_nodelay = True
            )
        }

        # rospy Publishers for JointCommand topics
        self.comm_publishers = {
            'left': rospy.Publisher(
                self.comm_topics['left'],
                baxter_core_msgs.msg.JointCommand,
                queue_size = None,
                tcp_nodelay = True
            ),
            'right': rospy.Publisher(
                self.comm_topics['right'],
                baxter_core_msgs.msg.JointCommand,
                queue_size = None,
                tcp_nodelay = True
            )
        }

    def sprint(self, message):
        print('[' + self.node + '] %s' % message)

    def cleanup(self):
        self.control_queue = None
        self.cancel_queue = None

    def start(self):
        self.sprint('starting node...')
        rospy.init_node(self.node)

        # Enable Baxter
        robot = RobotEnable()
        robot.enable()

        rospy.on_shutdown(self.cleanup)
        self.sprint('Node running - Ctrl + C to shutdown')
        rospy.spin()
        self.sprint('Control Node running...')
        curr_time = time.time()
        while(True):
            if curr_time - time.time() == -1:
                curr_time = time.time()
                self._consume_cancel()
                self._consume_control()

    def _consume_control(self):
        try:
            self.sprint(self.control_queue.get_nowait())
        except:
            return

    def _consume_cancel(self):
        try:
            self.sprint(self.cancel_queue.get_nowait())
        except:
            return