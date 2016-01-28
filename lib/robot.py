#!/usr/bin/env python
import sys
import rospy
from lib.jsonparser import *
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
import time
import brics_actuator.msg
from lib.demomanager import *
import math
from threading import Thread
from std_msgs.msg import String

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


#
# Robotbase is used to send goals to the base
#
class RobotBase:
    #Initialise
    def __init__(self):
        #Log
        rospy.loginfo("Creating robot base controller");       
        #Publisher used to manually control the robot
        self.cmd_vel_publisher = rospy.Publisher('/move_base/cmd_vel',geometry_msgs.msg.Twist);
        #Subscribe to the move_base action server
        self.move_base_server = actionlib.SimpleActionClient('move_base',MoveBaseAction);
        #move base goal publisher
        #self.move_base_goal_publisher = rospy.Publisher('/move_base/goal',move_base_msgs.msg.MoveBaseActionGoal);                
        rospy.loginfo("Starting move_base action server..");
        #Wait unil the acton server is available
        self.move_base_server.wait_for_server(rospy.Duration(60));
        rospy.loginfo("Started move_base action server");
        #Created!    
        rospy.loginfo("Created robot base");
    #Process given cmdVel command
    def procCmdVel(self,twist):
        for i in range(30):
            self.cmd_vel_publisher.publish(twist)
    
    #Stop moving the base - cancel all goals
    def Stop(self):
        #Now stop the robot
        rospy.loginfo("Attempting to stop robot")
        self.procCmdVel(geometry_msgs.msg.Twist())        

    #Create a goal message
    def CreateGoal(self,x,y,z,w):
        #Create msg object
        g = MoveBaseGoal()
        g.target_pose.header.frame_id = "base_link";
        g.target_pose.header.stamp = rospy.Time.now()
        g.target_pose.pose.position.x = x; #Move in X axis by meters
        g.target_pose.pose.position.y = y; #Move in Y axis by meters 
        g.target_pose.pose.position.z = z; #Move in Z axis by meters
        g.target_pose.pose.orientation.w = w; #We need to specify an orientation > 0
        return g
    #Move base in direction
    def Move(self,lx,ly,az,amount):
        #Create the twist message
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = lx
        twist.linear.y = ly
        twist.angular.z = az
        self.procCmdVel(twist)        
        #Robot is moving 1 m/s, so we should wait for specified given distance
        time.sleep(amount)
        #Stop the robot after waiting
        self.Stop()
    def _Move(self,lx,ly,az):
        #Create the twist message
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = lx
        twist.linear.y = ly
        twist.angular.z = az
        self.procCmdVel(twist)        

    #Move the base to a goal
    def MoveTo(self,x,y,z):
        #Create the goal 
        goal = self.CreateGoal(x,y,z,1.0);
        #Send the robot to the goal
        rospy.loginfo("Moving robot towards goal");
        self.move_base_server.send_goal(goal);
        #get result
        goalresult= self.move_base_server.wait_for_result(rospy.Duration(50));
        #stop when reached
        self.Stop();
#Min class is used for triggering an emergency stop
class EStop:
    #Initialise
    def __init__(self):
        #We can subscribe to a ros topic which holds whether the estop was pressed
        self.sub = rospy.Subscriber("chatter",String,self._Callback)
        #We also need a publisher
        self.pub = rospy.Publisher("chatter",String)
    #Callback function
    def _Callback(self,data):
        print data        
    #Trigger the emergency stop
    def Trigger(self):
        self.pub.publish(String("ON"))

#
# Primary Youbot class
#
class Youbot:
    #Initialise
    def __init__(self):
        rospy.loginfo("Initialising youbot")
        #Init moveit_commander
        moveit_commander.roscpp_initialize(sys.argv)
        #Init rospy
        rospy.init_node('youbot',anonymous=True)
        #Init robot object
        self.robot = moveit_commander.RobotCommander()
        #Init scene object
        self.scene = moveit_commander.PlanningSceneInterface()
        #robot base
        self.base = RobotBase();
        #robot arm        
        self.arm = RobotArm();
        #Youbot has been initialised
        rospy.loginfo("Youbot initialised")      
        #Finally - print the initial state of the youbot        
        self.Print_State()
        #Estop used for emergency stops
        self.estop = EStop()

    #############################################
    # GENERAL, ROBOT SPECIFIC COMMANDS
    #############################################
    def EmergencyStop(self):
        self.estop.Trigger()
    
    #############################################
    # BASE SPECIFIC COMMANDS
    #############################################
    
    #print the current robot state
    def Print_State(self):
        rospy.loginfo("Displaying current robot state")
        print self.robot.get_current_state()
        print " "
    #Drive the robot
    def Drive(self,lx,ly,az,amount):
        #Create a twist message
        self.base.Move(lx,ly,az,amount);
    #Drive the robot to a goal
    def DriveTo(self,x,y,z):
        #Create appropriate ROS message
        self.base.MoveTo(x,y,z);
    #Stop the robot
    def Stop(self):
        #Stop the arm
        self.arm.Stop();
        #stop the base
        self.base.Stop();
        
        
    #############################################
    # ARM SPECIFIC COMMANDS
    #############################################
    #Attempt to reach a pre-specified position using the robot arm
    def Reach(self,name):
        self.arm.MoveTo(name)
    #Grab (Close gripper)
    def Grab(self):
        self.arm.CloseGripper()
    #Drop (Open gripper)
    def Drop(self):
        self.arm.OpenGripper()
    #Print the status of the gripper
    def PrintGripperStatus(self):
        self.arm.PrintGripperStatus()
    #Check if the gripper is open
    def IsGripperOpen(self):
        return (self.arm.GetGripperStatus() == True)
    #Check if the gripper is closed
    def IsGripperClosed(self):
        return (self.arm.GetGripperStatus() == False)
    
#
# Robot controller
#
class RobotController:
    #Initialise
    def __init__(self):
        #Define the youbot object
        self.robot = Youbot();
        #Demo manager
        self.demo_manager = DemoManager(self.robot)
        self.data = None
        self.EMERGENCY_STOP = False
        #Thread used for processing data
        self.thread = Thread(target=self._ThreadFunc,args = ())
        #Start process data checks
        self.Start()
    #Halt execution -- acts as an emergency stop
    def Halt(self):
        self.robot.EmergencyStop()
    #Process incoming data
    def Process(self,data):
        #Create JSON object using given data
        #json_data = JSONObject(data);
        
        #Get the commands from the json data
        #commands = json.getData('commands');
        commands_json = JSONObject(data.getData('attribute'))
        commands = commands_json.getData('commands')

        #These variables are used to check for a condition
        condition_current = ' ' #The current condition to check
        condition_valid = True #The result of the condition
    
        
        #Cycle through, and manage the given commands
        for command in commands:
            #Ensure the robot is stopped before running more commands
            self.robot.Stop()               
            #
            # We may get, and print command info 
            #
            _command = JSONObject(command);
            _type = _command.getData('type');
            _att = _command.getData('attribute');
            _val = _command.getData('value');
            print "Command Given"
            print "TYPE: "  + _type;
            print "ATTRIBUTE: " + _att;
            print "VALUE: " + _val;

            #Print the status of the gripper - for debugging
            self.robot.PrintGripperStatus()

            
            
            #Check if the given data is a condition
            if(_type == "COND"):
                rospy.loginfo("Found condition")
                #Initially - the condition isn't valid
                condition_valid = False
                #Check the type of the condition
                if(_att == "GRIPPERSTATE"):
                    rospy.loginfo("Gripper state condition")
                    #Check the state of the gripper
                    #Which state are we checking for?
                    state_check = str(_val)
                    if(state_check=="OPEN"):
                        print "Checking gripper open condition"
                        #Check if the gripper is open
                        if(self.robot.IsGripperOpen()):
                            #Gripper is open
                            condition_valid = True
                    elif(state_check=="CLOSED"):
                        print "Checking gripper closed condition"
                        #Check if the gripper is closed
                        if(self.robot.IsGripperClosed()):
                            #Gripper is closed
                            condition_valid = True
                            
            #We may carry on if condition is valid
            if(condition_valid == True):
                rospy.loginfo("Condition is valid, executing command..")
            
            #
            # Now we need to check the given type, and use the data appropriately
            #
            #Application request command
                if(_type == "APPDATA"):
                    # -- Now process the application data, and save it to file
                    xml_file = open(_data + ".xml","wb");
                    xml_file.write(_data02);
                    xml_file.close();
                    print xml_file
                #Demo request command
                if(_type == "DEMO"):
                    print "Demo command"
                    # -- Demo start
                    if(_att == "START"):
                        print "Demo start request"
                        #Get the demo name
                        name = str(_val)
                        rospy.loginfo("Trying to start demo using given name: " + str(_val))
                        self.demo_manager.LaunchDemo(name)
                    # --Demo stop
                    if(_att == "STOP"):
                        print "Demo stop request"
                        #Stop the currently running demo
                        self.demo_manager.StopDemo()
                        Keyboard.Restore()
            
                #Move type command
                if(_type == "MOVE"):
                        print "Move command";
                        #Get amount value
                        amount = float(int(_val));
                        print "Amount: " + str(amount);
                        if(_att == "FORWARDS"):
                            print "Move forward command";
                            self.robot.DriveTo(amount,0,0);
                            #Process the data here - move the robot forward
                        if(_att == "BACK"):
                            print "Move backward command";
                            self.robot.DriveTo(-amount,0,0);
                            #Move the robot back
                        if(_att == "LEFT"):
                            print "Move left command";
                            self.robot.DriveTo(0,amount,0);
                            #Move the robot left
                        if(_att == "RIGHT"):
                            print "Move right command";
                            self.robot.DriveTo(0,-amount,0);
                            #Move the robot right
                #Rotate type command
                if(_type == "ROTATE"):
                        if(_att == "RIGHT"):
                            #Rotate the robot right
                            print "Rotate right command";
                            self.robot.Drive(0,0,0,1,amount);
                        if(_att == "LEFT"):
                            #Rotate the robot left
                            print "Rotate left command";
                            self.robot.Drive(0,0,0,-1,amount);
                #Move arm type command
                if(_type == "MOVEARM"):
                        #Is this is a 'move to pre-defined position' command?
                        if(_att == "DEFPOS"):
                            #If so - attempt to move the robot to the given position name
                            #self.robot.arm.ToStandardJointSpaceGoal(str(_val))
                            self.robot.arm.MoveTo(str(_val))
                #Rotate joint command
                if(_type == "ROTATEJOINT"):
                        #Rotate the joint
                        joint_name = str(_att)
                        value = float(_val)
                        self.robot.arm.SetJointValue(self.robot.arm.JointIdByName(joint_name),value)
                #Set gripper command
                if(_type =="GRIPPER"):
                        #What type of gripper command is this?
                        #Set gripper status command
                        if(_att == "SET"):
                            #Has the user chosen to open, or close the gripper?
                            choice = str(_val)
                            if(choice == "OPEN"):
                                self.robot.Drop()
                            elif(choice == "CLOSE"):
                                 self.robot.Grab()
            
                #halt type command
                if(_type == "HALT"):
                    print "Halt command";
                    self.robot.Stop();
            
                #Pause before starting next command
                rospy.sleep(0.2);
            else:
                print "Unable to execute command.. condition is not valid"
                
        #Stop the robot once execution has finished
        self.robot.Stop();
        #Reset data
        self.data = None
    #Set data
    def SetData(self,data):
        rospy.loginfo("Setting process data")
        if(data!=None):
            self.data = data
    #Thread function
    def _ThreadFunc(self):
        while True:
            if self.data != None:
                rospy.loginfo("Found process data")
                self.Process(self.data)
                time.sleep(1)
    #Start processing data
    def Start(self):
        rospy.loginfo("Starting process thread")
        self.thread.deamon = True
        self.thread.start()
    def Shutdown(self):
        rospy.signal_shutdown("Done!")
