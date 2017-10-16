#!/usr/bin/env python

import rospy
from unity_ros_msgs.msg import VRCommand
from baxter_core_msgs.msg import JointCommand
from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest
)
from geometry_msgs.msg import (
    PoseStamped,
)

def callback(comm):
    msg = PoseStamped()
    msg.header.seq = 0
    msg.header.stamp = rospy.get_rostime()
    msg.header.frame_id = 'base'
    msg.pose = comm.pose  
 
    arr = SolvePositionIKRequest()
    arr.pose_stamp.append(msg)
    arr.seed_mode = 0
    
    print arr

    left_ik_addr = '/ExternalTools/left/PositionKinematicsNode/IKService'
    right_ik_addr = '/ExternalTools/right/PositionKinematicsNode/IKService'
 
    if rospy.get_param('/robot/unityros/movelock') == True:
        return

    try:
        left_ik = rospy.ServiceProxy(left_ik_addr, SolvePositionIK)
        right_ik = rospy.ServiceProxy(right_ik_addr, SolvePositionIK)
        
        if comm.limb == 'left':
            ik = left_ik(arr)
        else:
            ik = right_ik(arr)

        right_limb = rospy.Publisher('/robot/limb/right/joint_command', JointCommand, queue_size=1)
        left_limb = rospy.Publisher('/robot/limb/left/joint_command', JointCommand, queue_size=1)

        message = JointCommand()
        message.mode = 1
        message.command = ik.joints[0].position
        message.names = ik.joints[0].name
        rospy.loginfo(message)
        right_limb.publish(message)
        left_limb.publish(message)  

    except rospy.ServiceException, e:
        print 'Service call failed: %s' % e

def cancelCallback(comm):
    curr_val = rospy.get_param('/robot/unityros/movelock')

    if curr_val:
        rospy.set_param('/robot/unityros/movelock', False)
    else:
        rospy.set_param('/robot/unityros/movelock', True) 

def main():

    print 'Starting controller node'
    rospy.init_node('unity_ros_controller')
    
    rate = rospy.Rate(800) # running at max safe speed 800Hz

    left_ik_addr = '/ExternalTools/left/PositionKinematicsNode/IKService'
    right_ik_addr = '/ExternalTools/right/PositionKinematicsNode/IKService'

    rospy.set_param('/robot/unityros/movelock', False)

    print 'Starting to listen for unity commands'
    rospy.Subscriber('/robot/unity_command', VRCommand, callback)
    rospy.Subscriber('/robot/unity_command_cancel', VRCommand, cancelCallback)

    right_limb = rospy.Publisher('/robot/limb/right/joint_command', JointCommand, queue_size=1)
    left_limb = rospy.Publisher('/robot/limb/left/joint_command', JointCommand, queue_size=1)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
