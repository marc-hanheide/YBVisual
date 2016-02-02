#!/usr/bin/env python
import sys
import rospy
from lib.ybvisual.jsonparser import *
import moveit_commander
import moveit_msgs.msg
import actionlib
import geometry_msgs.msg
import control_msgs.msg
from geometry_msgs import *
from brics_actuator.msg import JointPositions
from brics_actuator.msg import JointValue
import move_base_msgs.msg
from move_base_msgs.msg import *
from actionlib_msgs.msg import *
from std_msgs.msg import *
import brics_actuator.msg

#
# Robotarm is used to control the robot arm
#
class RobotArm:
    #Gripper
    class Gripper:
        #Initialise
        def __init__(self):
            self.state = 'open'
            self._GripperCmdPublisher = rospy.Publisher("/arm_1/gripper_controller/position_command",JointPositions, queue_size=1)
            self._GripperCmdSubscriber = rospy.Subscriber("/arm_1/gripper_controller/position_command",JointPositions,self.Callback)
            self.joint_name = 'gripper_finger_joint_r'
        #Callback is used to check the state of the gripper
        def Callback(self,data):
            j_cmd_length = len(data.positions)
            j_cmd = data.positions[0].value
            print j_cmd
            rospy.loginfo("Recevied gripper data: " + str(j_cmd))
            if(j_cmd == 0.0115):
                self.state = 'open'
            else:
                self.state = 'closed'
            print "The gripper is " + self.state
        #Prints the status of the gripper
        def PrintStatus(self):
            rospy.loginfo("Gripper status")
            rospy.loginfo(str(self.state))
        #Open gripper
        def Open(self):
            rospy.loginfo("Opening gripper")
            self.Set(0.0115)
        #Close gripper
        def Close(self):
            rospy.loginfo("Closing gripper")
            self.Set(0)
        #Toggle gripper
        def Toggle(self,flag):
            rospy.loginfo("Toggling gripper")
            if(flag==True):
                self.Open() #true == Open
            else:
                self.Close() #false == Close
        #Set joint value
        def Set(self,value):
            grp_cmd = JointPositions()
            j_cmd = JointValue()
            j_cmd.joint_uri = self.joint_name
            j_cmd.unit = 'm'
            j_cmd.value = value
            grp_cmd.positions.append(j_cmd)
            print "Sending gripper command: " + str(j_cmd.value)
            self._GripperCmdPublisher.publish(grp_cmd)
        #Check if the gripper is open
        def IsOpen(self):
            if(self.state == 'open'):
                print "Gripper is open"
                return True
        #Check if the gripper is closed
        def IsClosed(self):
            if(self.state == 'closed'):
                print "Gripper is closed"
                return False
        #Return the gripper state as a boolean value
        def CheckState(self):
            if(self.state == 'open'):
                print "Gripper is open"
                return True #True == open
            else:
                print "Gripper is closed"
                return False #False == closed
    #Initialise
    def __init__(self):
        #Log
        rospy.loginfo("Creating robot arm controller");
        #Move group for arm joints
        self.group = moveit_commander.MoveGroupCommander("arm_1")
        #Display trajectory publisher
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory)
        #Arm cmd publisher
        self._ArmCmdPublisher = rospy.Publisher("/arm_1/arm_controller/position_command",JointPositions,queue_size=1)
        #Arm joint names
        self.joint_names = ['arm_joint_1','arm_joint_2','arm_joint_3','arm_joint_4','arm_joint_5']
        self.joint_limits = [[0.0100692,5.84014],[0.0100692,2.61799],[-5.02655,-0.015708],[0.0221239,3.4292],[0.110619,5.64159]]
        #Gripper
        self.gripper = RobotArm.Gripper()
    #Moves to specified move group
    def MoveTo(self,name):
        rospy.loginfo("Moving to group: " + name)
        self.group.set_named_target(str(name))
        self.group.go()
	#Pause execution until the robot reaches the target group
        rospy.sleep(5)
    #Stop moving the arm
    def Stop(self):
        self.group.stop()
    def SetJointValue(self,joint_id,value):
        #Check given joint id
        if(joint_id > 0  and joint_id <= 5):
            #Get the joint limits
            joint_limit_min = self.joint_limits[joint_id-1][0]
            joint_limit_max = self.joint_limits[joint_id-1][1]
            #Check that given value is in joint limit range
            if(value > joint_limit_min and value < joint_limit_max):
                vals = self.group.get_current_joint_values()
                vals[joint_id-1] = float(value)
                self.group.set_joint_value_target(vals)
                self.group.go()
            #Else return error
            else:
                print "Value out of joint range: " + str(value) + ", for joint: "  + str(joint_id)
                print "Min: " + str(joint_limit_min)
                print "Max: " + str(joint_limit_max)
        #Else return error
        else:
            print "Invalid joint_id: " + str(joint_id)
        rospy.sleep(1)
    def SetJointValues(self,j1,j2,j3,j4,j5):
        self.SetJointValue(1,j1) #joint 1
        self.SetJointValue(2,j2) #joint 2
        self.SetJointValue(3,j3) #joint 3
        self.SetJointValue(4,j4) #joint 4
        self.SetJointValue(5,j5) #joint 5
    def JointIdByName(self,name):
        rospy.loginfo("Finding joint id using given name: " + str(name))
        for index in range(len(self.joint_names)):
            if(str(name)==str(self.joint_names[index])):
                rospy.loginfo("Found id : " + str(index+1) + " for joint name: " + str(name))
                return index+1
    #
    # Gripper functions
    #
    
    #Toggle the gripper
    def ToggleGripper(self,flag):
        self.gripper.Toggle(flag)
    #Open the gripper
    def OpenGripper(self):
        self.gripper.Open()
    #Close the gripper
    def CloseGripper(self):
        self.gripper.Close()
    #Print gripper status
    def PrintGripperStatus(self):
        self.gripper.PrintStatus()
    #Get the status of the gripper
    def GetGripperStatus(self):
        return self.gripper.CheckState()