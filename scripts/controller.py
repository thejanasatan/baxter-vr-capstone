#!/usr/bin/env python

import rospy
from multiprocessing import Queue, Process

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
    Point,
    Quaternion,
) 

from baxter_core_msgs.msg import (
    JointCommand,
    EndpointState,
)

from sensor_msgs.msg import (
    JointState,
)

from std_msgs.msg import (
    Header,
)

"""
Baxter IK Solver
"""
from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest,
)

import time

class BaxterNode():
    def __init__(self, con_queue, can_queue):
        self.control_queue = con_queue
        self.cancel_queue = can_queue
        self.node = 'rsdk_baxter_unity'

        self.ik_solvers = {}

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

        # rospy Publishers for IKService topics
        self.ik_publishers = {
            'left': rospy.Publisher(
                self.ik_topics['left'], 
                JointState, 
                queue_size = 1,
                tcp_nodelay = True
            ),
            'right':  rospy.Publisher(
                self.ik_topics['right'],
                JointState,
                queue_size = 1,
                tcp_nodelay = True
            )
        }

        # rospy Publishers for JointCommand topics
        self.comm_publishers = {
            'left': rospy.Publisher(
                self.comm_topics['left'],
                JointCommand,
                queue_size = 1,
                tcp_nodelay = True
            ),
            'right': rospy.Publisher(
                self.comm_topics['right'],
                JointCommand,
                queue_size = 1,
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

        # Start IK Solver proxy
        self._start_ik_solver()

        rospy.on_shutdown(self.cleanup)
        self.sprint('Node running - Ctrl + C to shutdown')
        self.sprint('Control Node running...')
        curr_time = time.time()
        while(True):
            self._consume_cancel()
            self._consume_control()

    def _start_ik_solver(self):
        try:
            # Wait to make sure the services are actually running
            rospy.wait_for_service('/ExternalTools/left/PositionKinematicsNode/IKService', timeout=2)
            rospy.wait_for_service('/ExternalTools/right/PositionKinematicsNode/IKService', timeout=2)

            self.ik_solvers = {
                'left': rospy.ServiceProxy(self.ik_topics['left'], SolvePositionIK, persistent=True),
                'right': rospy.ServiceProxy(self.ik_topics['right'], SolvePositionIK, persistent=True)
            }
        except rospy.ROSException:
            rospy.logError('IKSolver Services not up or something')

    def _consume_control(self):
        try:
            # IDIOT - YOURE GETTING A DICTIONARY: NOT A STRING SO QUIT TRYING TO SPLIT SHIT
            message = self.control_queue.get_nowait()
            
            # IK Solver Message Creation
	    ik_req = SolvePositionIKRequest()

	    hdr = Header(stamp=rospy.Time.now(), frame_id='base')
	    
	    pose = {
	    	'left': PoseStamped(
			header=hdr,
			pose=Pose(
				position=Point(
					x=0,
					y=0,
					z=0,
				),
				orientation=Quaternion(
					x=0,
					y=0,
					z=0,
					w=0,
				),
			),
		),
	    }

	    ikreq.pose_stamp.append(poses['left'])
	    rospy.wait_for_service(self.ik_topics['left'], 5.0)
	    resp = self.ik_solvers['left'](ikreq)
	    self.sprint(resp)
	except:
	    return
	    

    def _consume_cancel(self):
        try:
            message = self.cancel_queue.get_nowait()
        except:
            return
