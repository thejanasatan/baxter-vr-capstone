#!/usr/bin/env python

# Import ROS dependencies
import rospy

# Import package dependencies
from message_types import NodeHealthCheck

"""
ROSUnity Message Broker
-----------------------
Handles the message passing between the Unity Controller and the actionlib/Motion planning and execution nodes
"""
class ROSUnityBroker:

    def __init__(self, robot_ns):
        """
        Initialise the node - controls ros actions
        ros_unity_controller node can receive positioning/pose information from unity over the network
        and controls a robot's systems via the internal message queues
        """
        rospy.init_node('ros_unity_broker')
        
        """
        Spin up the ros node
        Registers itself from the Master so that the other nodes can discover it if they need to
        """
        rospy.spin()
        rospy.InfoLog("READY: ros_unity_broker node")

    """
    @param receivers []string
    @returns responses []bool
    
    Pings the receiving nodes i.e. Movement controller nodes for readiness test
    """
    def ping_receivers(self, receivers):
        return [for receiver in receivers rospy.pub(NodeHealthCheck.PING)]