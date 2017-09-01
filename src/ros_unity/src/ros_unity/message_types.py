#!usr/bin/env python

"""
message_types.py
-----------------
Convenience module that defines the types of messages passed into the ROS Graph
"""

"""
HEALTH CHECKS
"""
class NodeHealthCheck:
    PING = 'ROS_UNITY_PING'
    ROS_READY = 'ROS_UNITY_READY'