#!/usr/bin/env python

import rospy

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

"""
Baxter Path Solving service
"""
from baxter_core_msgs.srv import (
    SolvePositionIK as ik_solver
)

class BaxterNode():
    def __init__(self, con_queue, can_queue):
        self.control_queue = con_queue
        self.cancel_queue = can_queue
        self.node = 'rsdk_baxter_unity'

        # Namespace config for topics
        self.base_ns = '/robot/limb'
        self.sides = ['left', 'right']

        # Topic sets
        self.endpoint_comm_topics = [for side in self.sides self.base_ns + '/' + side + '/commanded_endpoint_state']
        self.endpoint_state_topics = [for side in self.sides self.base_ns + '/' + side + '/endpoint_state']

        # IKSolver topics
        self.ik_topics = {
            left: '/ExternalTools/left/PositionKinematicsNode/IKService',
            right: '/ExternalTools/right/PositionKinematicsNode/IKService',
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