import rospy
import baxter_interface
import actionlib
import sys

from control_msgs.msg import (
    FollowJointTrajectoryAction,
    FollowJointTrajectoryGoal,
)

from baxter_interface import (
    RobotEnable,
)

from trajectory_msgs.msg import (
    JointTrajectoryPoint,
)

class BaxterNode():
  def __init__(self, limb, control_queue, cancel_queue):
    ns = 'robot/limb/' + limb + '/'
    
    self.sprint('starting node....')
    rospy.init_node('rsdk_baxter_unity')
    
    robot = RobotEnable()
    robot.enable()

    rospy.on_shutdown(self.cleanup)

    self.control_queue = control_queue
    self.cancel_queue = cancel_queue

    self._limb_interface = baxter_interface.limb.Limb(limb)

    self._client = actionlib.SimpleActionClient(
        ns + "follow_joint_trajectory",
        FollowJointTrajectoryAction,
    )
    self._goal = FollowJointTrajectoryGoal()
    self._goal_time_tolerance = rospy.Time(0.1)
    self._goal.goal_time_tolerance = self._goal_time_tolerance
    server_up = self._client.wait_for_server(timeout=rospy.Duration(10.0))
    if not server_up:
      rospy.logerr("Timed out waiting for Joint Trajectory"
                    " Action Server to connect. Start the action server"
                    " before running example.")
      rospy.signal_shutdown("Timed out waiting for Action Server")
      sys.exit(1)
    self._clear_goal(limb)

  def _add_point(self, positions, time):
    point = JointTrajectoryPoint()
    point.positions = copy(positions)
    point.time_from_start = rospy.Duration(time)
    self._goal.trajectory.points.append(point)

  def _run_goal(self):
    self._goal.trajectory.header.stamp = rospy.Time.now()
    self._client.send_goal(self._goal)

  def _cancel_goal(self):
    self._client.cancel_goal()

  def _wait_for_result(self, timeout=15.0):
    self._client.wait_for_result(timeout=rospy.Duration(timeout))

  def _result(self):
    return self._client.get_result()

  def _clear_goal(self, limb):
    self._goal = FollowJointTrajectoryGoal()
    self._goal.goal_time_tolerance = self._goal_time_tolerance
    self._goal.trajectory.joint_names = [limb + '_' + joint for joint in \
      ['s0', 's1', 'e0', 'e1', 'w0', 'w1', 'w2']]

  def cleanup():
    self.control_queue = None
    self.cancel_goal = None

  def start(self):
    while True:
      self.consume_cancel()
      self.consume_control()

  def sprint(self, message):
    print('[rsdk_baxter_unity] ' + message)

  def consume_control(self):
    try:
      message = self.control_queue.get_nowait()

      point = message['position']
      orientation = message['rotation']

      self.sprint(point)

    except:
      return

  def consume_cancel(self):
    return
