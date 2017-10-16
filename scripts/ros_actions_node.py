#!/usr/bin/env python

import rospy, sys
from unity_ros_msgs.msg import VRCommand
from baxter_core_msgs.msg import JointCommand
from baxter_core_msgs.srv import (
    SolvePositionIK,
    SolvePositionIKRequest
)
from geometry_msgs.msg import (
    PoseStamped,
)

import baxter_interface

def try_float(x):
    try:
        return float(x)
    except ValueError:
        return None


def clean_line(line, names):
    line = [try_float(x) for x in line.rstrip().split(',')]
    #zip the values with the joint names
    combined = zip(names[1:], line[1:])
    #take out any tuples that have a none value
    cleaned = [x for x in combined if x[1] is not None]
    #convert it to a dictionary with only valid commands
    command = dict(cleaned)
    left_command = dict((key, command[key]) for key in command.keys()
                        if key[:-2] == 'left_')
    right_command = dict((key, command[key]) for key in command.keys()
                         if key[:-2] == 'right_')
    return (command, left_command, right_command, line)

def map_file(lines, loops=1):

    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')
    rate = rospy.Rate(1000)

    l = 0
    # If specified, repeat the file playback 'loops' number of times
    while loops < 1 or l < loops:
        i = 0
        l += 1
        print("Moving to start position...")

        firstline = lines[1]
        _cmd, lcmd_start, rcmd_start, _raw = clean_line(lines[1], keys)
        start_time = rospy.get_time()
        for values in lines[1:]:
            i += 1
            loopstr = str(loops) if loops > 0 else "forever"
            sys.stdout.write("\r Record %d of %d, loop %d of %s" %
                             (i, len(lines) - 1, l, loopstr))
            sys.stdout.flush()

            cmd, lcmd, rcmd, values = clean_line(values, keys)
            #command this set of commands until the next frame
            while (rospy.get_time() - start_time) < values[0]:
		if rospy.get_param('/robot/unityros/movelock'):
		    return False
                if rospy.is_shutdown():
                    print("\n Aborting - ROS shutdown")
                    return False
                if len(lcmd):
                    left.set_joint_positions(lcmd)
                if len(rcmd):
                    right.set_joint_positions(rcmd)
                rate.sleep()
        print
    return True

def callback(comm):
    if rospy.get_param('/robot/unityros/movelock') == True:
        return
    with open('/home/mb/baxter-movements/baxter-recording-vertical.csv', 'r') as f:
	lines = f.readlines()
    global keys
    keys = lines[0].rstrip().split(',')

    map_file(lines)

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
