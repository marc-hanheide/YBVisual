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
    #Custom arm state struct
    class ArmState:
        #Initialise
        def __init__(self,name,j1,j2,j3,j4,j5):
            self.name = name #state name
            self.j1 = j1 #joint 1
            self.j2 = j2 #joint 2
            self.j3 = j3 #joint 3
            self.j4 = j4 #joint 4
            self.j5 = j5 #joint 5
    #Custom arm state store
    class ArmStateStore:
        container = []             
        #Add arm state
        @staticmethod
        def AddState(_state):
            if _state != None:            
                RobotArm.ArmStateStore.container.append(_state)
        #GEt arm state
        @staticmethod
        def GetState(name):
            #Only check if given name is valid
            if(name!=None):
                cont = RobotArm.ArmStateStore.container
                rospy.loginfo("Searching for arm state: " + str(name))
                for i in range(0,len(cont)):
                    if str(name) == str(cont[i].name):
                            rospy.loginfo("Found arm state: " + str(name))
                            return RobotArm.ArmStateStore.container[i]
                return None
            else:
                rospy.loginfo("Cannot search for null name state")
                return None
        #Return if container has state
        @staticmethod
        def HasState(name):
            #Only check if given name is valid
            if name != None:
                result = RobotArm.ArmStateStore.GetState(name)
                if(result!=None):
                    rospy.loginfo("Store has state: " + str(name))
                    return True #Found state!
                else:
                    rospy.loginfo("Store does not have state: " + str(name))
                    return False #State does not exist
        @staticmethod
        def AddDefaults():
            RobotArm.ArmStateStore.AddState(RobotArm.ArmState("search",3.1,1.5,-1.43523,2,2.8))
            
                
        
    
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
        RobotArm.ArmStateStore.AddDefaults()
    #Moves to specified move group
    def MoveTo(self,name):
        try:
            rospy.loginfo("Moving to group: " + name)
            #First try the arm state store
            if(RobotArm.ArmStateStore.HasState(name)):
                #Get the state
                state = RobotArm.ArmStateStore.GetState(name)
                #Attempt to move to the state
                self.SetJointVals(state.j1,state.j2,state.j3,state.j4,state.j5)
                self.group.go()
                print self.group.get_current_joint_values()
                rospy.sleep(5)
            else:
                self.group.set_named_target(str(name))
                self.group.go()
                #Pause execution until the robot reaches the target group
                rospy.sleep(5)
        except Exception as e:
            print "Unable to move to target: "+ str(name)
            print e
    #Moves to specified arm state
    def MoveToState(self,_state):
        try:
            if _state != None:
                arm_cmd = brics_actuator.msg.JointPositions()
                arm_cmd.positions.append(self.ArmJointValue(self.joint_limits[0],_state.j1))
                arm_cmd.positions.append(self.ArmJointValue(self.joint_limits[1],_state.j2))
                arm_cmd.positions.append(self.ArmJointValue(self.joint_limits[2],_state.j3))
                arm_cmd.positions.append(self.ArmJointValue(self.joint_limits[3],_state.j4))
                arm_cmd.positions.append(self.ArmJointValue(self.joint_limits[4],_state.j5))
                print arm_cmd
                self._ArmCmdPublisher.publish(arm_cmd)
                rospy.sleep(1)
        except Exception as e:
            print e
    def ArmJointValue(self,uri,value):
        j_cmd = brics_actuator.msg.JointValue()
        j_cmd.joint_uri = uri
        j_cmd.unit = 'rad'
        j_cmd.value = value
        return j_cmd
            
    #Moves arm to random position        
    def Random(self):
        rospy.loginfo("Moving arm to random position")
        self.group.set_random_target()
        self.group.go()
        #Pause execution while target is reached
        rospy.sleep(5)
    #Stop moving the arm
    def Stop(self):
        self.group.stop()
    def SetJointVals(self,j1,j2,j3,j4,j5):
        try:
            vals = self.group.get_current_joint_values()
            vals[0] = j1
            vals[1] = j2
            vals[2] = j3
            vals[3] = j4
            vals[4] = j5
            print vals
            self.group.set_joint_value_target(vals)
        except Exception as e:
            print e
    
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
                print "Set value for joint " + str(joint_id)
                print "With value " + str(value)
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