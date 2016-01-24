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
import move_base_msgs.msg
from move_base_msgs.msg import *
from actionlib_msgs.msg import *
from std_msgs.msg import *
import time
import brics_actuator.msg
from lib.demomanager import *
import math

#
# Robotarm is used to control the robot arm
#
class RobotArm:
    #Gripper
    class Gripper:
        #Initialise
        def __init__(self):
            self.group = moveit_commander.MoveGroupCommander("arm_1_gripper")
        #Open gripper
        def Open(self):
            rospy.loginfo("Opening gripper")
            self.group.set_named_target("open")
            self.group.go()
            rospy.sleep(3)
        #Close gripper
        def Close(self):
            rospy.loginfo("Closing gripper")
            self.group.set_named_target("close")
            self.group.go()
            rospy.sleep(3)
        #Toggle gripper
        def Toggle(self,flag):
            rospy.loginfo("Toggling gripper")
            if(flag==True):
                self.Open() #true == Open
            else:
                self.Close() #false == Close   
    #Initialise
    def __init__(self):
        #Log
        rospy.loginfo("Creating robot arm controller");
        #Move group for arm joints
        self.group = moveit_commander.MoveGroupCommander("arm_1")
        #Display trajectory publisher
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory)        
        #Arm joint names
        self.joint_names = ['arm_joint_1','arm_joint_2','arm_joint_3','arm_joint_4','arm_joint_5']
        #Gripper
        self.gripper = RobotArm.Gripper()
    #Moves to specified move group
    def MoveTo(self,name):
        rospy.loginfo("Moving to group: " + name)
        self.group.set_named_target(str(name))
        self.group.go()
        rospy.sleep(3)
    #Toggle the gripper
    def ToggleGripper(self,flag):
        self.gripper.Toggle(flag)
    #Open the gripper
    def OpenGripper(self):
        self.gripper.Open()
    #Close the gripper
    def CloseGripper(self):
        self.gripper.Close()


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
    #Process incoming data
    def Process(self,data):
        #Create JSON object using given data
        #json_data = JSONObject(data);
        
        #Get the commands from the json data
        #commands = json.getData('commands');
        commands_json = JSONObject(data.getData('attribute'))
        commands = commands_json.getData('commands')
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
            if(_type== "MOVEARM"):
                    #Is this is a 'move to pre-defined position' command?
                    if(_att == "DEFPOS"):
                        #If so - attempt to move the robot to the given position name
                        self.robot.arm.ToStandardJointSpaceGoal(str(_val))
            
            #halt type command
            if(_type == "HALT"):
                print "Halt command";
                self.robot.Stop();
            
            #Pause before starting next command
            rospy.sleep(0.2);
                
        #Stop the robot once execution has finished
        self.robot.Stop();