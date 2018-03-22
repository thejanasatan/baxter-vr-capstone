#! /usr/bin/env python

import rospy, os, sys
from random import randint
from unite_conference.msg import clash
import baxter_interface

def listener():
    global running
    running = False

    rospy.Subscriber("/robot/unity_command_cancel", clash, interrupt)
    rospy.Subscriber("/robot/unity_command_start", clash, cmdstart)
    rospy.Subscriber("/robot/unity_command_end", clash, cmdend)

    global moves, clashed, exiting, action_index
    exiting = False
    clashed = 0
    action_index=randint(1,12)
    while not exiting:
        while running:
            movement()
        map_file(moves["0.csv"])
        

def movement():
    global clashed, moves, action_index
    action_index = (action_index + randint(-2,2) + clashed * 6)%12
    if action_index == 0:
        action_index = 1
    print "\n"+ str(action_index)
    map_file(moves[str(action_index)+".csv"])

def exiting():
    global interrupt, moves, exiting
    interrupt = False
    exiting = True
    map_file(moves["0.csv"])

def interrupt(state):
    global interrupt, clashed
    interrupt = True
    clashed = 0

def cmdstart(state):
   global running
   running = True

def cmdend(state):
   global running
   running = False

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
    global interrupt, clashed, exiting

    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')
    rate = rospy.Rate(1000)
    l = 0
    # If specified, repeat the file playback 'loops' number of times
    while loops < 1 or l < loops:
        i = 0
        l += 1

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
                if interrupt and not exiting:
                    interrupt = False
                    return False
                if len(lcmd):
                    left.set_joint_positions(lcmd)
                if len(rcmd):
                    right.set_joint_positions(rcmd)
                rate.sleep()
    clashed = 1
    return True

if __name__ == '__main__':
    path_moves = "/home/mb/vxlab_ws/src/unite_conference/motions/" 
    moves = {}

    for file in os.listdir(path_moves):
        with open(path_moves+file, 'r') as f:
            lines = f.readlines()
            moves[file] = lines
        keys = lines[0].rstrip().split(',')

    rospy.init_node("attack_server")
    rospy.on_shutdown(exiting)
    listener()
