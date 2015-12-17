#!/usr/bin/env python
import sys
import rospy
import json
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from geometry_msgs import *
import move_base_msgs.msg
from std_msgs.msg import *


#
# Primary Youbot class
#
class Youbot:
    #Init
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
        #Init move group object
        self.group = moveit_commander.MoveGroupCommander("arm_1")
        #Display trajectory publisher
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory)
        #move base cmd publisher
        self.move_base_cmdvel_publisher = rospy.Publisher('/move_base/cmd_vel',geometry_msgs.msg.Twist);
        #move base goal publisher
        self.move_base_goal_publisher = rospy.Publisher('/move_base/goal',move_base_msgs.msg.MoveBaseActionGoal);
        #Youbot has been initialised
        rospy.loginfo("Youbot initialised")      
        #Finally - print the initial state of the youbot        
        self.Print_State()
    #print the current robot state
    def Print_State(self):
        rospy.loginfo("Displaying current robot state")
        print self.robot.get_current_state()
        print " "
    #Drive the robot
    def Drive(self,lx,ly,lz,ax,ay,az):
        #Create a twist message
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = lx
        twist.linear.y = ly
        twist.linear.z = lz
        twist.angular.x = ax
        twist.angular.y = ay
        twist.angular.z = az
        #log event
        rospy.loginfo("Driving Youbot")
        #now publish
        for i in range(30):
           self.move_base_cmdvel_publisher.publish(twist)
           rospy.sleep(0.1) # 30*0.1 = 3.0
    #Stop the robot
    def Stop(self):
        self.Drive(0,0,0,0,0,0);

#
# JSON Object
#
class JSONObject:
    #Initialise
    def __init__(self,_jsondata):
        self.data = json.loads(_jsondata)
        print "Created JSON object"
    def getData(self,att):
        return self.data[att];



#
# Robot controller
#
class RobotController:
    #Initialise
    def __init__(self):
        #Define the youbot object
        self.robot = Youbot();
        self.Processing = False;
    #Process incoming data
    def Process(self,data):
        #Create JSON object using given data
        json = JSONObject(data);
        #Get the commands from the json data
        commands = json.getData('commands');
        #Cycle through, and manage the given commands
        for command in commands:
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
            if(_type == "APPDATA"):
                # -- Now process the application data, and save it to file
                xml_file = open(_data + ".xml","wb");
                xml_file.write(_data02);
                xml_file.close();
                print xml_file
            #Move type command
            if(_type == "MOVE"):
                    print "Move command";
                    if(_att == "FORWARDS"):
                        print "Move forward command";
                        self.robot.Drive(1,0,0,0,0,0);
                        #Process the data here - move the robot forward
                    if(_att == "BACK"):
                        print "Move backward command";
                        self.robot.Drive(-1,0,0,0,0,0);
                        #Move the robot back
                    if(_att == "LEFT"):
                        print "Move left command";
                        self.robot.Drive(0,1,0,0,0,0);
                        #Move the robot left
                    if(_att == "RIGHT"):
                        print "Move right command";
                        self.robot.Drive(0,-1,0,0,0,0);
                        #Move the robot right
            #Rotate type command
            if(_type == "ROTATE"):
                    if(_att == "RIGHT"):
                        print "Rotate right command";
                        #Rotate the robot right
                    if(_att == "LEFT"):
                        print "Rotate left command";
                        #Rotate the robot left
            #halt type command
            if(_type == "HALT"):
                print "Halt command";
                self.robot.Stop();
            
            rospy.sleep(0.2);
                
            
        self.robot.Stop();